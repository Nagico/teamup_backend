from django.db import models


class Activity(models.Model):
    title = models.CharField(max_length=35, blank=True, verbose_name="赛事名")

    introduction = models.TextField(blank=True, verbose_name="赛事简介")

    # [{"name": xxx, "url": xxx}, ...]
    information = models.JSONField(default=list, verbose_name="官网和通知")

    logo = models.ImageField(
        blank=True, null=True, upload_to=r"activity\logo", verbose_name="赛事logo"
    )

    start_time = models.DateField(verbose_name="开始时间")
    end_time = models.DateField(verbose_name="结束时间")

    # [{"name": xxx, "date": xxx}, ...]
    time_node = models.JSONField(default=list, verbose_name="时间节点")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        app_label = "activities"
        db_table = "zq_activity"
        verbose_name = "赛事"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
