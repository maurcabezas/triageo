"""
LangGraph nodes — one function per node, each takes TriageState and returns
a partial state dict that LangGraph merges into the running state.

Node order: classify_ticket → retrieve_context → route_ticket
            → decide_human_review → finalize_output
"""

from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from app.graph.state import TriageState
from app.core.llm import get_chat_model
from app.core.config import settings
from app.services.knowledge_base import KnowledgeBase
from app.services.database import save_ticket

# KB loaded once at module import — shared across all requests
_kb = KnowledgeBase(settings.kb_dir)


# ---------------------------------------------------------------------------
# Routing table — deterministic, no LLM involved
# ---------------------------------------------------------------------------

ROUTING_TABLE: dict[str, str] = {
    "privacy_request": "privacy-ops",
    "spam_abuse": "trust-safety",
    "billing": "billing-support",
    "product_bug": "engineering",
    "feature_request": "product",
    "account_access": "account-ops",
    "documentation_gap": "content-team",
    "unknown": "support-general",
}


# ---------------------------------------------------------------------------
# Structured output schema for the classify node
# ---------------------------------------------------------------------------

class ClassificationResult(BaseModel):
    """Structured output returned by the LLM classification call."""

    category: Literal[
        "privacy_request",
        "spam_abuse",
        "billing",
        "product_bug",
        "feature_request",
        "account_access",
        "documentation_gap",
        "unknown",
    ]
    priority: Literal["low", "medium", "high", "critical"]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(description="One or two sentences explaining the classification.")


# ---------------------------------------------------------------------------
# System prompt for classification
# ---------------------------------------------------------------------------

CLASSIFY_SYSTEM_PROMPT = """You are a support ticket triage assistant.
Analyze the ticket and classify it into exactly one category.

Categories:
- privacy_request  : GDPR/CCPA data deletion, access requests, data exports
- spam_abuse       : spam, harassment, abuse, Terms of Service violations
- billing          : payment failures, refunds, subscription changes, invoices
- product_bug      : software bugs, crashes, errors, unexpected behavior
- feature_request  : requests for new features or product improvements
- account_access   : login failures, password resets, locked or suspended accounts
- documentation_gap: unclear documentation, missing guides, broken help links
- unknown          : cannot determine from the information provided

Priority levels:
- low      : general question, minor inconvenience, workaround exists
- medium   : moderate impact, affects workflow but not blocking
- high     : significant impact, no workaround, customer frustrated
- critical : service down, data loss risk, legal obligation, SLA breach

Set confidence between 0.0 (completely uncertain) and 1.0 (absolutely certain).
Write a brief, factual reasoning in one or two sentences."""


# ---------------------------------------------------------------------------
# Node 1 — classify_ticket
# ---------------------------------------------------------------------------

def classify_ticket(state: TriageState) -> dict:
    """
    Call the LLM to classify the ticket.
    Returns: category, priority, confidence, reasoning.
    """
    llm = get_chat_model()
    structured_llm = llm.with_structured_output(ClassificationResult)

    user_content = (
        f"Subject: {state['subject']}\n\n"
        f"Description: {state['description']}\n\n"
        f"Customer tier: {state['customer_tier']}"
    )

    result: ClassificationResult = structured_llm.invoke([
        SystemMessage(content=CLASSIFY_SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ])

    return {
        "category": result.category,
        "priority": result.priority,
        "confidence": result.confidence,
        "reasoning": result.reasoning,
    }


# ---------------------------------------------------------------------------
# Node 2 — retrieve_context  (Phase 3 stub)
# ---------------------------------------------------------------------------

def retrieve_context(state: TriageState) -> dict:
    """
    Retrieve relevant knowledge-base snippets for the ticket.

    Phase 3: keyword overlap search over data/knowledge_base/ markdown docs.
    Phase later: replace with vector embedding search.
    """
    snippets = _kb.retrieve(state["subject"], state["description"])
    return {"retrieved_context": snippets}


# ---------------------------------------------------------------------------
# Node 3 — route_ticket
# ---------------------------------------------------------------------------

def route_ticket(state: TriageState) -> dict:
    """
    Map classified category to the appropriate team queue.
    Pure function — no LLM call.
    """
    team = ROUTING_TABLE.get(state["category"], "support-general")
    return {"recommended_team": team}


# ---------------------------------------------------------------------------
# Node 4 — decide_human_review
# ---------------------------------------------------------------------------

def decide_human_review(state: TriageState) -> dict:
    """
    Apply rule-based logic to determine if a human must review the ticket.

    Rules (any match → requires_human_review = True):
    - Confidence below 0.70
    - Priority is critical
    - Enterprise customer with high or critical priority
    - Category is privacy_request (legal obligation)
    """
    low_confidence = state["confidence"] < 0.70
    critical = state["priority"] == "critical"
    enterprise_high = (
        state["customer_tier"] == "enterprise"
        and state["priority"] in ("high", "critical")
    )
    privacy_legal = state["category"] == "privacy_request"

    requires_review = any([low_confidence, critical, enterprise_high, privacy_legal])
    return {"requires_human_review": requires_review}


# ---------------------------------------------------------------------------
# Node 5 — finalize_output
# ---------------------------------------------------------------------------

def finalize_output(state: TriageState) -> dict:
    """
    Final pass-through node.
    Phase 5: Persists the completed triage result to SQLite.
    """
    save_ticket(state)
    return {}
