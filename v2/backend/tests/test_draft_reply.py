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
    assert "intent" in data
    assert "confidence" in data
    assert "needs_review" in data
    assert isinstance(data["draft"], str)
    assert isinstance(data["intent"], str)
    assert isinstance(data["confidence"], float)
    assert isinstance(data["needs_review"], bool)


def test_draft_reply_rejects_empty_email_body():
    response = client.post(
        "/draft-reply",
        json={"email_body": ""},
    )

    assert response.status_code == 422

def test_detects_meeting_intent():
    response = client.post(
        "/draft-reply",
        json={"email_body": "Hi there! Can we reschedule our meeting to next week Tuesday?"},
    )
    data=response.json()

    assert response.status_code==200
    assert data["intent"]=="meeting"
    assert data["needs_review"] is True

def test_detects_thanks_intent():
    response = client.post(
        "/draft-reply",
        json={"email_body": "Hi there! I really appreciate the feedback. \nCheers,\nTyler"},
    )
    data=response.json()
    assert response.status_code==200
    assert data["intent"]=="thanks"
    assert data["needs_review"] is False

def test_detects_follow_up_intent():
    response = client.post(
        "/draft-reply",
        json={"email_body": "Hi there! I'm just following up on my previous message!"},
    )
    data=response.json()
    assert response.status_code==200
    assert data["intent"]=="follow_up"
    assert data["needs_review"] is True

def test_detects_unknown_intent():
    response = client.post(
        "/draft-reply",
        json={"email_body": "Hi there! Please see me in my office"},
    )
    data=response.json()
    assert response.status_code==200
    assert data["intent"]=="unknown"
    assert data["needs_review"] is True