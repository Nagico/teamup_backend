from activities.models import Activity
from django.db import models
from users.models import User

from server.utils.models.users import CommonUserInformation


class Team(models.Model):
    """
    队伍
    """

    name = models.CharField(max_length=30, blank=True, verbose_name="队伍名")

    activity = models.ForeignKey(
        Activity,
        null=True,
        on_delete=models.CASCADE,
        related_name="teams",
        verbose_name="所属赛事",
    )

    leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leader_teams",
        verbose_name="队长",
    )

    introduction = models.TextField(blank=True, verbose_name="队伍简介")

    teacher = models.CharField(max_length=10, blank=True, verbose_name="指导老师")

    # [{"type": ..., "value": ...}, ...]
    # types: phone, email, wechat, qq
    contact = models.JSONField(default=list, verbose_name="联系方式")

    public = models.BooleanField(default=False, verbose_name="是否公开")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        app_label = "teams"
        db_table = "zq_team"
        verbose_name = "队伍"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.leader}-{self.name}"


class TeamDemand(models.Model):
    """
    队伍需求
    """

    role = models.ForeignKey(
        "roles.Role",
        on_delete=models.CASCADE,
        related_name="team_demands",
        verbose_name="角色",
    )

    number = models.IntegerField(blank=True, verbose_name="招募人数")

    detail = models.TextField(blank=True, verbose_name="招募详情")

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="demands",
        verbose_name="招募需求",
    )

    class Meta:
        app_label = "teams"
        db_table = "zq_team_demand"
        verbose_name = "招募需求"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.team}-{self.role}"


class TeamMember(CommonUserInformation):
    """
    队伍成员
    """

    # null: 手动输入, 非 null: 自动导入（内容优先级更高）
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="join_teams",
        verbose_name="用户",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="队伍",
    )

    role = models.ForeignKey(
        "roles.Role",
        on_delete=models.SET_NULL,
        null=True,
        related_name="team_members",
        verbose_name="角色",
    )

    class Meta:
        app_label = "teams"
        db_table = "zq_team_member"
        verbose_name = "队伍成员"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.user is None:
            return f"{self.team}-{self.nickname}"
        else:
            return f"{self.team}-{self.user}"
