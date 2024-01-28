from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Feature, Goal, Schedule, Task, Theme


class ScheduleInline(GenericTabularInline):
    model = Schedule


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    inlines = (ScheduleInline,)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    inlines = (ScheduleInline,)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    inlines = (ScheduleInline,)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = (ScheduleInline,)
