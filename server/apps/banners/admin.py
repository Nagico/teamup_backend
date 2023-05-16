from banners import models
from django.contrib import admin


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ["id", "title", "subtitle", "score"]
    list_display_links = ["id", "title", "subtitle"]
    search_fields = ["title", "subtitle"]
    ordering = ["-score"]
