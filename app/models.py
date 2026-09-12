from typing import ClassVar

from django.db import models


class StudentOnboarding(models.Model):
    SUPPORT_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("reading", "Reading"),
        ("math", "Math"),
        ("speech", "Speech"),
        ("none", "None"),
    ]

    student_id = models.CharField(max_length=32, unique=True)
    student_name = models.CharField(max_length=120)
    age = models.PositiveSmallIntegerField()
    has_learning_difficulty = models.BooleanField()
    support_required = models.CharField(max_length=20, choices=SUPPORT_CHOICES)
    parent_email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["-created_at"]
