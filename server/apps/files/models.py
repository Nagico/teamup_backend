from django.db import models


class File(models.Model):
    """
    文件
    """

    name = models.CharField(max_length=255, verbose_name="文件名", blank=True)
    file = models.FileField(
        upload_to="files/", verbose_name="文件", blank=True, null=True
    )
    ext = models.CharField(max_length=10, verbose_name="文件扩展名", blank=True)
    size = models.IntegerField(verbose_name="文件大小", default=0)

    user = models.ForeignKey(
        "users.User",
        related_name="files",
        on_delete=models.CASCADE,
        verbose_name="用户",
    )

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        app_label = "files"
        db_table = "zq_file"
        verbose_name = "文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}.{self.ext}"
