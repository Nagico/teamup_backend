from threading import Thread

from django.conf import settings


class ConsumeAsync(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __enter__(self):
        self.daemon = True
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def run(self) -> None:
        """
        线程开始
        :return:
        """
        from server.utils.rabbitmq import RabbitMQ

        mq = RabbitMQ(settings.RABBITMQ_URL)
        mq.start()

    def stop(self) -> None:
        """
        强制结束线程
        :return:
        """
        self.join()
