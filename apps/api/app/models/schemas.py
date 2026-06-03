from pydantic import BaseModel, Field
from typing import Literal


class TicketRequest(BaseModel):
    """Incoming support ticket payload."""

    subject: str = Field(..., min_length=1, max_length=500, description="Ticket subject line")
    description: str = Field(..., min_length=1, max_length=5000, description="Full ticket body")
    customer_tier: Literal["free", "pro", "enterprise"] = Field(
        "free", description="Customer subscription tier"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "subject": "I need to delete my account",
                    "description": "Please delete all my personal data under GDPR.",
                    "customer_tier": "free",
                }
            ]
        }
    }


class TriageResponse(BaseModel):
    """Structured triage decision returned by the API."""

    ticket_id: str = Field(..., description="Unique identifier for this triage run")
    subject: str
    customer_tier: Literal["free", "pro", "enterprise"] = Field("free", description="Customer subscription tier")
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
    recommended_team: str = Field(..., description="Team or queue to route this ticket to")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence in classification")
    requires_human_review: bool
    reasoning: str = Field(..., description="Brief explanation of the triage decision")
    retrieved_context: list[str] = Field(
        default_factory=list,
        description="KB article snippets retrieved for this ticket",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticket_id": "mock-0001",
                    "subject": "I need to delete my account",
                    "category": "privacy_request",
                    "priority": "high",
                    "recommended_team": "privacy-ops",
                    "confidence": 0.5,
                    "requires_human_review": True,
                    "reasoning": "Mock result — LangGraph workflow not yet connected.",
                }
            ]
        }
    }
