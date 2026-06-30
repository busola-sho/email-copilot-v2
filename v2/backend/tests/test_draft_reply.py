from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_draft_reply_endpoint_returns_valid_response():
    response = client.post(
        "/draft-reply",
        json={"email_body": "Hi, can we reschedule our meeting to Friday?"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "draft" in data
    assert "confidence" in data
    assert "needs_review" in data
    assert isinstance(data["draft"], str)
    assert isinstance(data["confidence"], float)
    assert isinstance(data["needs_review"], bool)


def test_draft_reply_rejects_empty_email_body():
    response = client.post(
        "/draft-reply",
        json={"email_body": ""},
    )

    assert response.status_code == 422