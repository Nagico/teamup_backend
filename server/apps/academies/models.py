from django.db import models


class Academy(models.Model):
    """
    学院信息
    """

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_academies",
        null=True,
        blank=True,
        verbose_name="父级",
    )
    level = models.IntegerField(default=0, verbose_name="级别")
    name = models.CharField(max_length=50, verbose_name="院系名称")

    class Meta:
        app_label = "academies"
        db_table = "zq_academy"
        verbose_name = "院系"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
