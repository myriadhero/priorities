from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

"""
This is the core of the priorities app. The app is meant to simplify decision
making about what to do next based on simple rules and context like time.

The app will have major themes like sleep, health, work, value-driven
activities, social, etc. with their own priorities. It will output certain
priorities and tasks based on the time of day, day of week, priority of the
theme, and other factors, like deadlines.

The app will also have a way to track progress on goals, features, and tasks,
and will have a way to track time spent on each task. It will also have a way
to switch priority based on mood/energy level.

The primary priorities will be sleep, health and fitness, value-driven
activities, learning and growing/healthy challenges, recovery, social and
relationships, and work. These will come pre-loaded with the app, but users
will be able to modify them and add their own.

Themes will be the top level areas of the app, they will have overall
priority and general schedules. themes can have Goals, Features, and Tasks.
For example, sleep theme can have just the one repeating task of sleeping
on time, and health and fitness can have a goal of running a marathon, the
goal is further broken down into features like training a specific theme, while
tasks are the actual workouts.

Goals are the main things that you want to accomplish, they can have features
and tasks. Goals are long term big vision items that can still be measured.

Features should be smaller, anywhere from less than 1 week to a month max. They should
be SMART.

Tasks are the smallest unit of work, they should be able to be completed in a
day or less, ideally under an hour. They should be SMART.
"""


class Schedule(models.Model):
    """
    As an example, to represent a task schedule that happens MWF 8am for 1 hour and 9pm for 1 hour,
    we would use 6 scheudle objects, 1 for each day morning and 1 for each day evening.

    TODO: when newly added schedules for the same object overlap, merge them,
    for now it's up to the user to not do that.
    """

    class WeekDays(models.IntegerChoices):
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

    start_at = models.TimeField()
    duration = models.DurationField()
    is_daily = models.BooleanField(default=False)
    weekday = models.IntegerField(choices=WeekDays, null=True, blank=True)

    # Allow linking to all other models
    # https://docs.djangoproject.com/en/5.0/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=models.Q(is_daily=True) | models.Q(weekday__isnull=False),
                name="daily_or_weekday",
                violation_error_message="Schedule must be either daily or on a specific weekday.",
            ),
        )

    def __str__(self):
        return f"{self.get_weekday_display()} {self.start_at} {self.duration}"


class Priority(models.IntegerChoices):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    TOP = 3


class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        help_text="Why is this theme important? How does it fit into your life? How do you feel about it?",
    )
    priority = models.IntegerField(default=Priority.LOW, choices=Priority)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    schedules = GenericRelation(Schedule, related_query_name="theme")

    def __str__(self) -> str:
        return f"Theme {self.name}"


class PrioritizedModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        help_text="Why is this important? How does it fit into your life? How do you feel about it?",
    )
    priority = models.IntegerField(default=Priority.LOW, choices=Priority)
    deadline = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Goal(PrioritizedModel):
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT)

    schedules = GenericRelation(Schedule, related_query_name="goal")

    def __str__(self) -> str:
        return f"Goal {self.name} for theme {self.theme.name}"


class Feature(PrioritizedModel):
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT)

    schedules = GenericRelation(Schedule, related_query_name="feature")

    def __str__(self) -> str:
        return f"Feature {self.name} for goal {self.goal.name}"


class Task(PrioritizedModel):
    feature = models.ForeignKey(Feature, on_delete=models.PROTECT, null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT, null=True, blank=True)

    schedules = GenericRelation(Schedule, related_query_name="task")

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=models.Q(feature__isnull=False) ^ models.Q(theme__isnull=False),
                name="feature_or_theme",
                violation_error_message="Task must be parented to either a feature or a theme, and not both.",
            ),
        )

    def __str__(self) -> str:
        return f"Task {self.name} for {'feature '+self.feature.name if self.feature else 'theme '+self.theme.name}"
