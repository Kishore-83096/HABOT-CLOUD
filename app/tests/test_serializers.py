import pytest

from app.serializers import StudentOnboardingSerializer

VALID_PAYLOAD = {
    "student_id": "STU-001",
    "student_name": "Example Student",
    "age": 12,
    "has_learning_difficulty": True,
    "support_required": "reading",
    "parent_email": "parent@example.com",
}


def test_valid_onboarding_payload_is_accepted():
    serializer = StudentOnboardingSerializer(data=VALID_PAYLOAD)

    assert serializer.is_valid(), serializer.errors


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("age", 0),
        ("age", 26),
        ("student_id", "001"),
        ("parent_email", "not-an-email"),
        ("support_required", "unknown"),
    ],
)
def test_invalid_values_are_rejected(field, value):
    payload = {**VALID_PAYLOAD, field: value}
    serializer = StudentOnboardingSerializer(data=payload)

    assert not serializer.is_valid()
    assert field in serializer.errors


def test_required_field_is_rejected_when_missing():
    payload = {key: value for key, value in VALID_PAYLOAD.items() if key != "student_id"}
    serializer = StudentOnboardingSerializer(data=payload)

    assert not serializer.is_valid()
    assert "student_id" in serializer.errors
