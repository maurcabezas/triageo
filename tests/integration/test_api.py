from unittest.mock import patch, MagicMock
from app.graph.nodes import ClassificationResult


def test_health_endpoint(client):
    """Test that the /health endpoint is live and returning correct info."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "triageo-api"


@patch("app.services.triage_service.triage_graph.invoke")
def test_triage_ticket_endpoint(mock_invoke, client):
    """Test POST /api/v1/triage with a valid ticket."""
    mock_invoke.return_value = {
        "ticket_id": "triage-12345",
        "subject": "Missing items in my order",
        "description": "My package arrived but it is missing the blue shoes.",
        "customer_tier": "free",
        "category": "billing",
        "priority": "medium",
        "confidence": 0.88,
        "reasoning": "Ticket concerns missing purchase items.",
        "retrieved_context": ["[docs] Shipping: details on missing orders."],
        "recommended_team": "billing-support",
        "requires_human_review": False,
    }

    payload = {
        "subject": "Missing items in my order",
        "description": "My package arrived but it is missing the blue shoes.",
        "customer_tier": "free"
    }

    response = client.post("/api/v1/triage", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["ticket_id"] == "triage-12345"
    assert data["customer_tier"] == "free"
    assert data["category"] == "billing"
    assert data["priority"] == "medium"
    assert data["confidence"] == 0.88
    assert data["requires_human_review"] is False
    assert data["recommended_team"] == "billing-support"
    assert data["reasoning"] == "Ticket concerns missing purchase items."
    assert data["retrieved_context"] == ["[docs] Shipping: details on missing orders."]

    mock_invoke.assert_called_once()


def test_triage_ticket_validation_error(client):
    """Test POST /api/v1/triage with invalid/missing fields to trigger custom 422 error handler."""
    # Subject is required, customer_tier must be one of free, pro, enterprise
    payload = {
        "description": "Valid description",
        "customer_tier": "invalid-tier"
    }

    response = client.post("/api/v1/triage", json=payload)
    assert response.status_code == 422
    
    data = response.json()
    assert data["detail"] == "Validation Failed"
    assert any("subject" in err for err in data["errors"])
    assert any("customer_tier" in err for err in data["errors"])


@patch("app.api.triage.get_history")
def test_triage_history_endpoint(mock_get_history, client):
    """Test GET /api/v1/triage/history retrieves triage history."""
    mock_get_history.return_value = [
        {
            "ticket_id": "triage-1111",
            "subject": "Billing issue",
            "description": "charged twice",
            "customer_tier": "pro",
            "category": "billing",
            "priority": "high",
            "confidence": 0.95,
            "requires_human_review": True,
            "reasoning": "Duplicate charge",
            "retrieved_context": [],
            "recommended_team": "billing-support",
            "created_at": "2026-06-03T12:00:00Z"
        }
    ]

    response = client.get("/api/v1/triage/history?limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["ticket_id"] == "triage-1111"
    assert data[0]["customer_tier"] == "pro"
    assert data[0]["category"] == "billing"
    assert data[0]["priority"] == "high"
    assert data[0]["confidence"] == 0.95
    assert data[0]["requires_human_review"] is True
    
    mock_get_history.assert_called_once_with(5)
