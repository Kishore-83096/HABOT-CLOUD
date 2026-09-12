import json

import pytest
from django.test import override_settings
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_onboarding_endpoint_accepts_valid_payload(api_client, tmp_path):
    with override_settings(LOCAL_DATA_DIR=tmp_path):
        response = api_client.post(
            "/api/onboarding/",
            {
                "student_id": "STU-002",
                "student_name": "API Student",
                "age": 10,
                "has_learning_difficulty": False,
                "support_required": "none",
                "parent_email": "parent@example.com",
            },
            format="json",
        )

    assert response.status_code == 201
    assert response.data["student_id"] == "STU-002"
    raw_records = (tmp_path / "d0_raw_landing.jsonl").read_text().splitlines()
    staged_records = (tmp_path / "d1_staged.jsonl").read_text().splitlines()
    assert json.loads(raw_records[0])["student_id"] == "STU-002"
    assert json.loads(staged_records[0])["support_required"] == "none"


@pytest.mark.django_db
def test_onboarding_endpoint_rejects_invalid_payload(api_client, tmp_path):
    with override_settings(LOCAL_DATA_DIR=tmp_path):
        response = api_client.post(
            "/api/onboarding/",
            {
                "student_id": "STU-003",
                "student_name": "Invalid Student",
                "age": 40,
                "has_learning_difficulty": False,
                "support_required": "none",
                "parent_email": "parent@example.com",
            },
            format="json",
        )

    assert response.status_code == 400
    assert "age" in response.data
    assert not (tmp_path / "d0_raw_landing.jsonl").exists()
    assert not (tmp_path / "d1_staged.jsonl").exists()
