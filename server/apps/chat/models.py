from django.db import models

from server.utils.choices.types import MessageType


class Message(models.Model):
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="send_messages",
        verbose_name="发送用户",
    )
    receiver = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name="接收用户",
    )

    content = models.TextField(verbose_name="内容")
    type = models.IntegerField(
        choices=MessageType.choices,
        default=MessageType.UNKNOWN,
        verbose_name="类型",
    )
    read = models.BooleanField(default=False, verbose_name="已读")
    create_time = models.DateTimeField(verbose_name="创建时间")

    class Meta:
        app_label = "chat"
        db_table = "zq_message"
        verbose_name = "消息"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]
