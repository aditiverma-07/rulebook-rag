import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.decision import DecisionType, DecisionResult, EvidenceItem

client = TestClient(app)

def test_api_and_decision_agree():
    query = "What happens if I lose my student ID card?"
    response = client.post("/ask", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "answered"

@patch('app.llm.LLM_API_KEY', '')
@patch('app.main.evaluate_evidence')
def test_fallback_not_covered(mock_eval):
    mock_eval.return_value = DecisionResult(
        type=DecisionType.NOT_COVERED,
        answer="The rulebook does not contain enough information to answer this question.",
        evidence=[],
        reason="Test reason"
    )
    with patch('app.llm.requests.post') as mock_post:
        response = client.post("/ask", json={"query": "Test query?"})
        data = response.json()
        assert data["type"] == "not_covered"
        assert data["answer"] == "The rulebook corpus does not contain enough information to answer this question."
        assert mock_post.call_count == 0

@patch('app.llm.LLM_API_KEY', '')
@patch('app.main.evaluate_evidence')
def test_fallback_answered_no_llm(mock_eval):
    mock_eval.return_value = DecisionResult(
        type=DecisionType.ANSWERED,
        answer="Mocked answer",
        evidence=[EvidenceItem(chunk_id="1", source="src", text="test", similarity=0.9)],
        reason="Test reason"
    )
    response = client.post("/ask", json={"query": "Test query?"})
    data = response.json()
    assert data["type"] == "answered"
    assert data["answer"] == "LLM is not configured. Grounded answer generation is unavailable."

@patch('app.llm.LLM_API_KEY', '')
@patch('app.main.evaluate_evidence')
def test_fallback_conflict_no_llm(mock_eval):
    mock_eval.return_value = DecisionResult(
        type=DecisionType.CONFLICT,
        answer="Mocked answer",
        evidence=[
            EvidenceItem(chunk_id="1", source="src", text="test1", similarity=0.9),
            EvidenceItem(chunk_id="2", source="src2", text="test2", similarity=0.8)
        ],
        reason="Test reason"
    )
    response = client.post("/ask", json={"query": "Test query?"})
    data = response.json()
    assert data["type"] == "conflict"
    assert data["answer"] == "LLM is not configured. The rulebook corpus contains conflicting provisions relevant to this question."
    assert len(data["evidence"]) == 2
