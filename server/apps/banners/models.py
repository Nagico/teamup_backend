from django.db import models


class Banner(models.Model):
    """
    轮播图推荐
    """

    title = models.CharField(max_length=40, verbose_name="标题")
    subtitle = models.CharField(default="", max_length=40, verbose_name="副标题")
    cover = models.ImageField(upload_to="banner", default="", verbose_name="封面")
    photo = models.ImageField(upload_to="banner", default="", verbose_name="图片")
    content = models.TextField(default="", verbose_name="内容")
    score = models.IntegerField(default=0, verbose_name="分数")

    class Meta:
        app_label = "banners"
        db_table = "zq_banner"
        verbose_name = "轮播图推荐"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"
