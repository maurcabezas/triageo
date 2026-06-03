"""
Triage service — Phase 2: LangGraph workflow.

Replaces the Phase 1 deterministic mock with a real LangGraph invocation.
The graph runs: classify → retrieve → route → review → finalize.
"""

import uuid
from app.models.schemas import TicketRequest, TriageResponse
from app.graph.state import TriageState
from app.graph.graph import triage_graph


def run_triage(ticket: TicketRequest) -> TriageResponse:
    """
    Execute the LangGraph triage workflow for a given ticket.

    Builds the initial state from the incoming request, invokes the
    compiled graph, and maps the final state to the API response schema.
    """
    ticket_id = f"triage-{uuid.uuid4().hex[:8]}"

    initial_state: TriageState = {
        "ticket_id": ticket_id,
        "subject": ticket.subject,
        "description": ticket.description,
        "customer_tier": ticket.customer_tier,
        # Fields populated by graph nodes — initialised to safe defaults
        "category": "",
        "priority": "",
        "confidence": 0.0,
        "reasoning": "",
        "retrieved_context": [],
        "recommended_team": "",
        "requires_human_review": True,
    }

    final_state: TriageState = triage_graph.invoke(initial_state)

    return TriageResponse(
        ticket_id=final_state["ticket_id"],
        subject=final_state["subject"],
        customer_tier=final_state["customer_tier"],
        category=final_state["category"],          # type: ignore[arg-type]
        priority=final_state["priority"],          # type: ignore[arg-type]
        recommended_team=final_state["recommended_team"],
        confidence=final_state["confidence"],
        requires_human_review=final_state["requires_human_review"],
        reasoning=final_state["reasoning"],
        retrieved_context=final_state["retrieved_context"],
    )
