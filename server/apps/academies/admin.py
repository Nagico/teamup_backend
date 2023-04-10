from academies import models
from django.contrib import admin


@admin.register(models.Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = ["id", "name", "level"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    list_filter = ["level", "parent"]
