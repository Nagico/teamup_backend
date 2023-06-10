from activities.models import Activity
from django.contrib import admin


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    list_per_page = 20
