from django.contrib import admin

from .models import Action, Area, Project


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username", "user__email")
    list_filter = ("user",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "area")
    search_fields = ("name", "user__username", "user__email", "area__name")
    list_filter = ("user", "area")


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "project", "started_at", "ended_at", "duration_seconds", "created_at")
    search_fields = ("description", "user__username", "user__email", "project__name")
    list_filter = ("user", "project", "started_at", "ended_at", "created_at")
