from django.db import models
from zq_django_util.utils.user.models import AbstractUser

from server.utils.models.users import CommonUserInformation


class User(AbstractUser, CommonUserInformation):
    """
    用户
    """

    # extra-checks-disable-next-line field-text-null
    openid = models.CharField(
        max_length=64, unique=True, null=True, verbose_name="微信openid"
    )

    union_id = models.UUIDField(
        unique=True, null=True, blank=True, verbose_name="自强union_id"
    )

    name = models.CharField(max_length=15, blank=True, verbose_name="姓名")
    avatar = models.ImageField(
        upload_to=r"user\avatar",
        default=r"user\avatar\default.jpg",
        verbose_name="头像",
    )

    # [{"type": ..., "value": ...}, ...]
    # types: phone, email, wechat, qq
    contact = models.JSONField(default=list, verbose_name="联系方式")
    student_id = models.CharField(max_length=20, blank=True, verbose_name="学号")

    favorite_teams = models.ManyToManyField(
        "teams.Team", related_name="users", blank=True, verbose_name="收藏的队伍"
    )

    favorite_activities = models.ManyToManyField(
        "activities.Activity",
        related_name="users",
        blank=True,
        verbose_name="收藏的活动",
    )

    class Meta:
        app_label = "users"
        db_table = "zq_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
