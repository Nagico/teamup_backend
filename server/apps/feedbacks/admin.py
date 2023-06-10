from django.contrib import admin
from feedbacks.models import Feedback, FeedbackFile


class FeedbackFileInline(admin.TabularInline):
    model = FeedbackFile
    extra = 0


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "type"]
    inlines = [FeedbackFileInline]
    list_per_page = 20
