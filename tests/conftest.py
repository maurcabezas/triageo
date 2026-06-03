import sys
from pathlib import Path

# Add apps/api to Python path so `app` module is importable by tests
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.graph.state import TriageState


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def base_state() -> TriageState:
    return {
        "ticket_id": "triage-test-id",
        "subject": "I have a billing problem with my invoice",
        "description": "I canceled my pro plan subscription last week, but I was still charged.",
        "customer_tier": "free",
        "category": "",
        "priority": "",
        "confidence": 0.0,
        "reasoning": "",
        "retrieved_context": [],
        "recommended_team": "",
        "requires_human_review": True,
    }


@pytest.fixture
def high_confidence_state(base_state) -> TriageState:
    return {
        **base_state,
        "category": "billing",
        "confidence": 0.92,
        "priority": "medium"
    }


@pytest.fixture
def low_confidence_state(base_state) -> TriageState:
    return {
        **base_state,
        "category": "unknown",
        "confidence": 0.45,
        "priority": "low"
    }
