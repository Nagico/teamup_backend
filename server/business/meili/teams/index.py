from requests import Request
from teams.models import Team
from zq_django_util.utils.meili.index import BaseIndex, BaseIndexHelper
from zq_django_util.utils.meili.response import SearchResult

from server.business.meili.teams.serializers import TeamIndexSerializer


class TeamIndex(BaseIndex):
    index_uid = "teams"

    filterable_attributes = [
        "public",
        "has_teacher",
        "activity_id",
        "role_ids",
    ]

    searchable_attributes = [
        "name",
        "activity",
        "leader",
        "introduction",
        "teacher",
        "contact",
    ]


class TeamIndexHelper(BaseIndexHelper):
    queryset = Team.objects.filter(
        public=True,
    )
    serializer_class = TeamIndexSerializer
    index_class = TeamIndex

    def construct_filter(
        self,
        has_teacher: bool = None,
        activity_ids: list[int] = None,
        role_ids: list[list] = None,
    ) -> list[str | list[str]]:
        """
        构造过滤条件
        :param has_teacher: 是否有指导老师
        :param activity_ids: 活动id（可多选）
        :param role_ids: 角色id（可多选）
        :return:
        """
        filters = ["public = true"]  # 用 AND 连接内部元素
        if has_teacher is not None:
            filters.append(f"has_teacher = {str(has_teacher).lower()}")
        if activity_ids is not None:
            activity_filter = []  # 用 OR 连接内部元素
            for activity_id in activity_ids:
                activity_filter.append(f"activity_id = {activity_id}")
            filters.append(activity_filter)
        if role_ids is not None:
            filters.append(f"role_ids IN {role_ids}")

        return filters

    def search_with_request(
        self,
        query: str,
        request: Request,
        has_teacher: bool = None,
        activity_ids: list[int] = None,
        role_ids: list[int] = None,
        **kwargs,
    ) -> SearchResult:
        return super().search_with_request(
            query,
            request,
            filter=self.construct_filter(has_teacher, activity_ids, role_ids),
            **kwargs,
        )
