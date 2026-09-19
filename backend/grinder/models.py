from django.conf import settings
from django.db import models
from django.db.models import Q


class Area(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="areas")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        related_name="projects",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actions")
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        related_name="actions",
        blank=True,
        null=True,
    )
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(started_at__isnull=False, ended_at__isnull=True, duration_seconds__isnull=True),
                name="one_running_action_per_user",
            ),
            models.CheckConstraint(
                condition=(
                    Q(started_at__isnull=False, ended_at__isnull=True, duration_seconds__isnull=True)
                    | Q(started_at__isnull=True, ended_at__isnull=True, duration_seconds__isnull=False)
                    | Q(started_at__isnull=False, ended_at__isnull=False, duration_seconds__isnull=False)
                ),
                name="action_has_valid_time_state",
            ),
            models.CheckConstraint(
                condition=Q(ended_at__isnull=True) | Q(ended_at__gte=models.F("started_at")),
                name="action_ends_after_start",
            ),
            models.CheckConstraint(
                condition=Q(duration_seconds__isnull=True) | Q(duration_seconds__gt=0),
                name="action_duration_positive",
            ),
        ]

    @property
    def is_running(self):
        return self.started_at is not None and self.ended_at is None and self.duration_seconds is None

    def __str__(self):
        return self.description or f"Action {self.pk or 'unsaved'}"
