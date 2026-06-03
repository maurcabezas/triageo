"""
LangGraph state definition.

TriageState is the single source of truth that flows through every node.
Nodes return a partial dict — LangGraph merges it into the running state.
"""

from typing import TypedDict


class TriageState(TypedDict):
    # --- Input fields (set on entry) ---
    ticket_id: str
    subject: str
    description: str
    customer_tier: str  # "free" | "pro" | "enterprise"

    # --- Populated by classify_ticket ---
    category: str
    priority: str
    confidence: float
    reasoning: str

    # --- Populated by retrieve_context (Phase 3) ---
    retrieved_context: list[str]

    # --- Populated by route_ticket ---
    recommended_team: str

    # --- Populated by decide_human_review ---
    requires_human_review: bool
