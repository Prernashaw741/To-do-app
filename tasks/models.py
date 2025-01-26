from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    