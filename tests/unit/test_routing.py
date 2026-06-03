from app.graph.nodes import route_ticket, decide_human_review


def test_category_routing_targets():
    """Verify that routing table maps support categories to correct teams."""
    state_billing = {"category": "billing"}
    assert route_ticket(state_billing) == {"recommended_team": "billing-support"}

    state_privacy = {"category": "privacy_request"}
    assert route_ticket(state_privacy) == {"recommended_team": "privacy-ops"}

    state_bug = {"category": "product_bug"}
    assert route_ticket(state_bug) == {"recommended_team": "engineering"}

    state_unknown = {"category": "unknown"}
    assert route_ticket(state_unknown) == {"recommended_team": "support-general"}


def test_escalation_low_confidence():
    """Confidence below 0.70 triggers human review."""
    state = {
        "confidence": 0.65,
        "priority": "low",
        "customer_tier": "free",
        "category": "billing"
    }
    assert decide_human_review(state) == {"requires_human_review": True}


def test_escalation_critical_priority():
    """Critical priority tickets always trigger human review."""
    state = {
        "confidence": 0.95,
        "priority": "critical",
        "customer_tier": "free",
        "category": "billing"
    }
    assert decide_human_review(state) == {"requires_human_review": True}


def test_escalation_privacy_request():
    """Privacy request category (GDPR/legal) always triggers human review."""
    state = {
        "confidence": 0.95,
        "priority": "low",
        "customer_tier": "free",
        "category": "privacy_request"
    }
    assert decide_human_review(state) == {"requires_human_review": True}


def test_escalation_enterprise_high():
    """High priority enterprise customers trigger human review."""
    state = {
        "confidence": 0.90,
        "priority": "high",
        "customer_tier": "enterprise",
        "category": "billing"
    }
    assert decide_human_review(state) == {"requires_human_review": True}


def test_auto_resolve_conditions():
    """High confidence, non-critical, non-privacy, non-enterprise tickets bypass human review."""
    state = {
        "confidence": 0.85,
        "priority": "high",
        "customer_tier": "free",
        "category": "billing"
    }
    assert decide_human_review(state) == {"requires_human_review": False}
