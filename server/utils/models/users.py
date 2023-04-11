from django.db import models

from server.utils.choices.types import DegreeType


class CommonUserInformation(models.Model):
    nickname = models.CharField(max_length=20, blank=True, verbose_name="昵称")

    academy = models.ForeignKey(
        "academies.Academy",
        related_name="%(class)s_users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="学院",
    )
    degree = models.IntegerField(
        choices=DegreeType.choices,
        default=DegreeType.UNKNOWN,
        verbose_name="学历",
    )
    grade = models.IntegerField(default=0, verbose_name="年级")

    introduction = models.TextField(blank=True, verbose_name="个人简介")

    # ["...", ...]
    experience = models.JSONField(default=list, verbose_name="经历")

    class Meta:
        abstract = True
