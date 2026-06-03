"""
LangGraph StateGraph definition.

Graph topology (Phase 2, linear):
  classify_ticket
      → retrieve_context
      → route_ticket
      → decide_human_review
      → finalize_output
      → END

Conditional branching will be added in later phases if needed
(e.g., escalation paths, re-classification on low confidence).
"""

from langgraph.graph import StateGraph, END
from app.graph.state import TriageState
from app.graph.nodes import (
    classify_ticket,
    retrieve_context,
    route_ticket,
    decide_human_review,
    finalize_output,
)


def _build_graph():
    graph = StateGraph(TriageState)

    # Register nodes
    graph.add_node("classify_ticket", classify_ticket)
    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("route_ticket", route_ticket)
    graph.add_node("decide_human_review", decide_human_review)
    graph.add_node("finalize_output", finalize_output)

    # Wire edges
    graph.set_entry_point("classify_ticket")
    graph.add_edge("classify_ticket", "retrieve_context")
    graph.add_edge("retrieve_context", "route_ticket")
    graph.add_edge("route_ticket", "decide_human_review")
    graph.add_edge("decide_human_review", "finalize_output")
    graph.add_edge("finalize_output", END)

    return graph.compile()


# Module-level compiled graph — built once on import, reused per request.
triage_graph = _build_graph()
