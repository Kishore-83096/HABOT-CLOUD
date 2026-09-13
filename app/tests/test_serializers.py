import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from app.dcyn import evaluate_onboarding
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


def test_dcyn_returns_binary_decisions_for_valid_payload():
    decisions = evaluate_onboarding(VALID_PAYLOAD)

    assert decisions == {
        "student_id": True,
        "student_name": True,
        "age": True,
        "has_learning_difficulty": True,
        "support_required": True,
        "parent_email": True,
        "payload": True,
    }


def test_dcyn_rejects_invalid_values_without_human_judgment():
    decisions = evaluate_onboarding({**VALID_PAYLOAD, "age": 26})

    assert decisions["age"] is False
    assert decisions["payload"] is False


def test_serializer_matches_onboarding_json_schema():
    schema_path = Path(__file__).parents[2] / "schemas" / "onboarding_schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    serializer = StudentOnboardingSerializer()

    assert set(serializer.fields) == set(schema["properties"])
    assert set(schema["required"]) == set(serializer.fields)
    assert not list(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(VALID_PAYLOAD)
    )
    assert (
        serializer.fields["student_id"].max_length
        == schema["properties"]["student_id"]["maxLength"]
    )
    assert (
        serializer.fields["student_name"].max_length
        == schema["properties"]["student_name"]["maxLength"]
    )
    assert (
        serializer.fields["parent_email"].max_length
        == schema["properties"]["parent_email"]["maxLength"]
    )
    assert set(serializer.fields["support_required"].choices) == set(
        schema["properties"]["support_required"]["enum"]
    )
