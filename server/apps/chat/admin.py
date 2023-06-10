from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "receiver", "type", "content", "is_read"]
    list_filter = ["sender", "receiver"]
    list_per_page = 20
