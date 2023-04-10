from typing import Any, Optional, Union

from celery import Task as CeleryTask
from celery.result import AsyncResult
from loguru import logger

from server.utils.choices.status import AsyncTaskStatus


def get_task_status(task: AsyncResult) -> dict[str, Any]:
    """
    获取任务状态
    :param task: 任务
    :return: 任务状态
    """
    info = task.info or {}
    if "result" in info:
        result = info.pop("result")
    else:
        result = None

    info["state"] = task.state

    response = {
        **info,
        "result": result,
    }
    return response


class Stages:
    """
    任务集
    """

    tasks: list["Task"]  # 任务列表
    current: int  # 当前任务索引

    parent_task: Union["Task", None] = None  # 父任务

    def __init__(self, parent_task: Union["Task", None] = None):
        """

        :param parent_task: 父任务
        """
        self.tasks = []
        self.current = -1
        self.parent_task = parent_task

    def to_dict(self):
        return [task.to_dict() for task in self.tasks]

    def __len__(self):
        return len(self.tasks)

    def __getitem__(self, item):
        return self.tasks[item]

    def __enter__(self):
        self.start_next()
        return self.current_stage

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.succeed_current()
        else:
            self.fail_current()

    @property
    def current_stage(self) -> "Task":
        """
        当前任务
        :return:
        """
        return self[self.current]

    @property
    def next_stage(self) -> Optional["Task"]:
        """
        下一个任务
        :return:
        """
        return self[self.current + 1] if self.current < len(self) - 1 else None

    @property
    def previous_stage(self) -> Optional["Task"]:
        """
        上一个任务
        :return:
        """
        return self[self.current - 1] if self.current > 0 else None

    def start_next(self, **kwargs) -> "Task":
        """
        开始下一个任务
        :return: 下一个任务
        """
        if self.parent_task.root.name is not None:
            if self.current >= 0:
                assert self.current_stage.is_finished, "当前子任务未完成"
            assert self.current < len(self.tasks) - 1, "子任务已完成"
        self.current += 1
        self.current_stage.start(**kwargs)

        self.current_stage.update_celery_state()
        return self.current_stage

    def succeed_current(self, **kwargs) -> "Task":
        """
        当前任务成功
        :return: 当前任务
        """
        self.current_stage.succeed(**kwargs)
        self.current_stage.update_celery_state()
        return self.current_stage

    def fail_current(self, **kwargs) -> "Task":
        """
        当前任务失败
        :return: 当前任务
        """
        self.current_stage.fail(**kwargs)
        self.current_stage.update_celery_state()
        return self.current_stage

    def add(self, name: str, detail: dict[str, Any] = None) -> "Task":
        """
        添加任务
        :param name: 任务名
        :param detail: 其他信息(dict)
        :return: 新增的任务
        """
        new_task = Task(name, self.parent_task.root.celery_task, detail)
        new_task.parent = self.parent_task
        new_task.root = self.parent_task.root
        new_task.index = len(self.tasks)

        self.tasks.append(new_task)
        new_task.update_celery_state()
        return new_task

    def add_group(self, data: list):
        """
        添加任务组
        :param data: 任务数据
        """
        for item in data:
            name = item.get("name")
            detail = item.get("detail")
            new_task = Task(name, self.parent_task.root.celery_task, detail)
            new_task.parent = self.parent_task
            new_task.root = self.parent_task.root
            new_task.index = len(self.tasks)

            self.tasks.append(new_task)
        self.parent_task.update_celery_state()


class Task:
    """
    任务
    """

    index: int = 0  # 索引
    name: str  # 名称
    state: AsyncTaskStatus  # 状态
    detail: dict[str, Any]  # 其他信息

    parent: Union["Task", None] = None  # 父任务
    root: Union["Task"]  # 根任务
    celery_task: Union[CeleryTask, None] = None  # celery任务

    stages: Stages  # 子任务集

    def __init__(
        self,
        name: str | None = None,
        celery_task: CeleryTask | None = None,
        detail: dict | None = None,
    ):
        """

        :param name: 任务名
        :param detail: 其他信息(dict)
        """
        self.name = name
        self.state = AsyncTaskStatus.PENDING
        self.detail = detail or {}
        self.stages = Stages(parent_task=self)
        self.celery_task = celery_task
        self.root = self

    def to_dict(self):
        return {
            "name": self.name,
            "state": self.state,
            **self.detail,
            # stages is none or a non-empty list
            "stages": None if len(self.stages) == 0 else self.stages.to_dict(),
        }

    @property
    def is_pending(self):
        return self.state == AsyncTaskStatus.PENDING

    @property
    def is_running(self):
        return self.state == AsyncTaskStatus.STARTED

    @property
    def is_finished(self):
        return self.state in [AsyncTaskStatus.SUCCESS, AsyncTaskStatus.FAILURE]

    @property
    def is_success(self):
        return self.state == AsyncTaskStatus.SUCCESS

    @property
    def is_failure(self):
        return self.state == AsyncTaskStatus.FAILURE

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.succeed()
        else:
            self.fail()

    def start(self, **kwargs):
        """
        任务开始
        :return:
        """
        self.state = AsyncTaskStatus.STARTED
        self.detail.update(kwargs)
        self.update_celery_state()

    def succeed(self, **kwargs):
        """
        任务成功
        :return:
        """
        self.state = AsyncTaskStatus.SUCCESS
        self.detail.update(kwargs)
        self.update_celery_state()

    def fail(self, **kwargs):
        """
        任务失败
        :return:
        """
        self.state = AsyncTaskStatus.FAILURE
        self.detail.update(kwargs)
        self.update_celery_state()

    def update_detail(self, **kwargs):
        """
        更新任务详情
        :param kwargs:
        :return:
        """
        self.detail.update(kwargs)
        self.update_celery_state()

    def update_celery_state(
        self, state: AsyncTaskStatus | None = None, meta: dict | None = None
    ):
        """
        更新celery任务状态
        :return:
        """
        if self.root.celery_task:
            self.root.celery_task.update_state(
                state=state or self.root.state,
                meta=meta or self.root.to_dict(),
            )
        logger.debug(
            f"update celery state: {self.root.state}, {self.root.to_dict()}"
        )

    def result(self, result: Any = None):
        """
        任务结果
        :return:
        """
        res = self.root.to_dict()
        res["result"] = result
        return res


if __name__ == "__main__":
    with Task("test") as task:
        task.start()
        task.stages.add("a")
        task.stages.add("b")
        task.stages.start_next()  # start a
        task.stages.succeed_current()  # finish a

        with task.stages as inner_task:
            inner_task.stages.add("b1")
            inner_task.stages.add("b2")
            inner_task.stages.start_next()  # start b1
            inner_task.stages.succeed_current()  # finish b1
            inner_task.stages.start_next()  # start b2
            inner_task.stages.succeed_current()  # finish b2

        task.stages.add("c")
        task.stages.start_next()  # start c
        task.stages.fail_current()  # finish c
