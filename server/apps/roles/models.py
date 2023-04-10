from django.db import models


class Role(models.Model):
    """
    队伍角色表
    """

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_roles",
        null=True,
        blank=True,
        verbose_name="父级角色",
    )
    name = models.CharField(max_length=30, blank=True, verbose_name="角色名")
    level = models.IntegerField(default=0, verbose_name="级别")
    description = models.TextField(blank=True, verbose_name="角色描述")

    class Meta:
        app_label = "roles"
        db_table = "zq_role"
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
