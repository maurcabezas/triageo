from fastapi import APIRouter
from app.models.schemas import TicketRequest, TriageResponse
from app.services.triage_service import run_triage
from app.services.database import get_history

router = APIRouter(prefix="/api/v1", tags=["triage"])


@router.post(
    "/triage",
    response_model=TriageResponse,
    summary="Triage a support ticket",
    description=(
        "Accepts a support ticket and returns a structured triage decision. "
        "Phase 1 returns a deterministic mock. Phase 2 will connect the LangGraph workflow."
    ),
)
def triage_ticket(ticket: TicketRequest) -> TriageResponse:
    return run_triage(ticket)


@router.get(
    "/triage/history",
    response_model=list[TriageResponse],
    summary="Get recent triage decisions",
    description="Returns the most recent support tickets processed by the system."
)
def triage_history(limit: int = 10) -> list[TriageResponse]:
    # Maps rows from database to the TriageResponse model list
    return get_history(limit)

