from typing import ClassVar

from rest_framework import serializers

from .models import StudentOnboarding


class StudentOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOnboarding
        extra_kwargs: ClassVar[dict] = {
            "student_id": {"validators": []},
        }
        fields: ClassVar[list[str]] = [
            "student_id",
            "student_name",
            "age",
            "has_learning_difficulty",
            "support_required",
            "parent_email",
        ]

    def validate_age(self, value):
        if value < 1 or value > 25:
            raise serializers.ValidationError("Age must be between 1 and 25.")
        return value

    def validate_student_id(self, value):
        if not value.startswith("STU-"):
            raise serializers.ValidationError("Student ID must start with STU-.")
        return value
