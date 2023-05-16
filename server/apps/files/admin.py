from django.contrib import admin
from files import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_per_page = 20  # 每页显示条数
    list_display = [
        "id",
        "__str__",
        "user",
        "update_time",
    ]  # 列表显示字段
    list_display_links = ["id", "__str__"]  # 列表可点击字段
    readonly_fields = ["create_time", "update_time"]  # 只读字段
    search_fields = ["id", "user__name"]  # 搜索字段
    list_filter = ["user"]  # 过滤器
    ordering = ["-update_time"]  # 排序

    fieldsets = (
        ("文件信息", {"fields": ("name", "ext", "size", "file")}),
        ("其他信息", {"fields": ("user", "create_time", "update_time")}),
    )


class FileInline(admin.TabularInline):
    model = models.File
    extra = 0
    readonly_fields = ["create_time", "update_time"]
    fields = [
        "name",
        "ext",
        "size",
        "file",
        "user",
        "create_time",
        "update_time",
    ]
