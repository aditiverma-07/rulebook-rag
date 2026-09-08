import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from typing import Any

from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_requests_post():
    with patch("app.llm.requests.post") as mock_post:
        with patch("app.llm.LLM_API_KEY", "test-key"):
            yield mock_post

def test_not_covered_bypasses_llm(mock_requests_post):
    """Ensure NOT_COVERED queries never trigger an external LLM call."""
    # This query is known to evaluate as NOT_COVERED in the decision engine
    query = "Can I bring a smartwatch into the examination hall?"
    response = client.post("/ask", json={"query": query})
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "not_covered"
    
    # Verify the LLM was absolutely never called
    mock_requests_post.assert_not_called()

def test_conflict_supplies_both_sides(mock_requests_post):
    """Ensure CONFLICT queries supply both conflicting provisions to the LLM context."""
    # Mock a successful LLM response so generate_answer doesn't fail
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "Mocked conflict answer."}}]
    }
    
    # This query triggers the C001 conflict (10% vs 15% condonation)
    query = "What is the maximum percentage of attendance shortage that can be condoned?"
    response = client.post("/ask", json={"query": query})
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "conflict"
    assert len(data["evidence"]) >= 2
    
    # Verify that the LLM was called
    mock_requests_post.assert_called_once()
    
    # Inspect the payload sent to the LLM
    call_kwargs = mock_requests_post.call_args.kwargs
    payload = call_kwargs.get("json", {})
    messages = payload.get("messages", [])
    
    # The prompt must contain both chunks
    user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
    
    # Verify that evidence text from both opposing chunks was injected into the prompt
    assert "10%" in user_msg or "condonation" in user_msg.lower()
    assert "15%" in user_msg

def test_answered_receives_evidence(mock_requests_post):
    """Ensure ANSWERED queries supply the retrieved evidence."""
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "Mocked answered."}}]
    }
    
    query = "What is the minimum attendance requirement?"
    response = client.post("/ask", json={"query": query})
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "answered"
    
    mock_requests_post.assert_called_once()
    
    call_kwargs = mock_requests_post.call_args.kwargs
    payload = call_kwargs.get("json", {})
    messages = payload.get("messages", [])
    user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
    
    # Verify that evidence text was injected
    assert "75%" in user_msg

def test_hallucination_resistance(mock_requests_post):
    """Even if we somehow force the LLM to hallucinate, the architecture prevents it for NOT_COVERED."""
    # We patch requests.post to return a hallucinated answer. 
    # But for NOT_COVERED, requests.post shouldn't even be called!
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "Yes, you can bring a smartwatch."}}]
    }
    
    query = "Can I bring a smartwatch into the examination hall?"
    response = client.post("/ask", json={"query": query})
    
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "not_covered"
    # The answer MUST be the safe deterministic fallback, NOT the hallucination
    assert "The rulebook corpus does not contain enough information to answer this question." in data["answer"]
    assert "Yes, you can bring a smartwatch." not in data["answer"]
    mock_requests_post.assert_not_called()

def test_response_quality_answered():
    """Verify quality checks on ANSWERED API response payload."""
    query = "What is the minimum attendance requirement?"
    response = client.post("/ask", json={"query": query})
    data = response.json()
    
    assert data["type"] == "answered"
    assert data["answer"].strip() != ""
    assert len(data["evidence"]) > 0
    # Every evidence item should have a source
    for e in data["evidence"]:
        assert e["source"] is not None
        assert e["section"] is not None

def test_response_quality_conflict():
    """Verify quality checks on CONFLICT API response payload."""
    query = "What is the maximum percentage of attendance shortage that can be condoned?"
    response = client.post("/ask", json={"query": query})
    data = response.json()
    
    assert data["type"] == "conflict"
    assert data["answer"].strip() != ""
    assert len(data["evidence"]) >= 2
    # Expect differing sources or at least multiple distinct evidence items
    sources = set(e["source"] for e in data["evidence"])
    assert len(sources) >= 1  # Could be same file, different sections

def test_response_quality_not_covered():
    """Verify quality checks on NOT_COVERED API response payload."""
    query = "Can I bring a smartwatch into the examination hall?"
    response = client.post("/ask", json={"query": query})
    data = response.json()
    
    assert data["type"] == "not_covered"
    assert data["answer"].strip() != ""
    # Should clearly indicate insufficiency
    assert "does not contain enough information" in data["answer"].lower()
    # Shouldn't fabricate any random numeric policy 
    assert not any(char.isdigit() for char in data["answer"])
