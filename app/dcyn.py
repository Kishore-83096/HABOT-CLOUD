from collections.abc import Mapping
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email

SUPPORT_VALUES = frozenset({"reading", "math", "speech", "none"})


def evaluate_onboarding(payload: Mapping[str, Any]) -> dict[str, bool]:
    """Return binary decisions for every onboarding rule."""
    student_id = payload.get("student_id")
    student_name = payload.get("student_name")
    age = payload.get("age")
    difficulty = payload.get("has_learning_difficulty")
    support_required = payload.get("support_required")
    parent_email = payload.get("parent_email")

    email_is_valid = False
    if isinstance(parent_email, str):
        try:
            validate_email(parent_email)
        except DjangoValidationError:
            pass
        else:
            email_is_valid = len(parent_email) <= 254

    decisions = {
        "student_id": (
            isinstance(student_id, str) and student_id.startswith("STU-") and len(student_id) <= 32
        ),
        "student_name": (isinstance(student_name, str) and 1 <= len(student_name) <= 120),
        "age": isinstance(age, int) and not isinstance(age, bool) and 1 <= age <= 25,
        "has_learning_difficulty": isinstance(difficulty, bool),
        "support_required": support_required in SUPPORT_VALUES,
        "parent_email": email_is_valid,
    }
    decisions["payload"] = all(decisions.values())
    return decisions
