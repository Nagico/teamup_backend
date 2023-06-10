from django.contrib import admin
from teams.models import Team, TeamDemand, TeamMember


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0


class TeamDemandInline(admin.TabularInline):
    model = TeamDemand
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "activity", "leader"]
    list_filter = ["activity", "leader"]
    search_fields = ["name"]
    list_per_page = 20
    inlines = [TeamMemberInline, TeamDemandInline]
