from django.contrib import admin

from . import models


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    list_filter = ["parent"]
