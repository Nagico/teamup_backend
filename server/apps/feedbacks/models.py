from django.db import models

from server.utils.choices.types import FeedbackType


class Feedback(models.Model):
    """
    反馈表
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="feedbacks",
        verbose_name="用户",
    )
    content = models.TextField(blank=True, verbose_name="反馈内容")
    type = models.IntegerField(
        choices=FeedbackType.choices,
        default=FeedbackType.UNKNOWN,
        verbose_name="反馈类型",
    )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        app_label = "feedbacks"
        db_table = "zq_feedback"
        verbose_name = "反馈"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user}-{self.content}"


class FeedbackFile(models.Model):
    """
    反馈文件
    """

    feedback = models.ForeignKey(
        "feedbacks.Feedback",
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="反馈",
    )
    file = models.FileField(
        upload_to="feedback/file/", verbose_name="反馈文件", blank=True, null=True
    )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        app_label = "feedbacks"
        db_table = "zq_feedback_file"
        verbose_name = "反馈文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.feedback}-{self.file}"
