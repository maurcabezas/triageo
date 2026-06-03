"""
SQLite database persistence service.
Phase 5 implementation.
"""

import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from app.core.config import settings

logger = logging.getLogger(__name__)


def get_db_connection() -> sqlite3.Connection:
    """Create a connection to the SQLite database."""
    # Ensure the parent directory exists (e.g. data/)
    db_path = Path(settings.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database schema, creating tables if they do not exist."""
    schema = """
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT PRIMARY KEY,
        subject TEXT NOT NULL,
        description TEXT NOT NULL,
        customer_tier TEXT NOT NULL,
        category TEXT NOT NULL,
        priority TEXT NOT NULL,
        recommended_team TEXT NOT NULL,
        confidence REAL NOT NULL,
        requires_human_review INTEGER NOT NULL,
        reasoning TEXT NOT NULL,
        retrieved_context TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """
    try:
        with get_db_connection() as conn:
            conn.execute(schema)
            conn.commit()
        logger.info("Database initialized successfully at %s", settings.db_path)
    except Exception:
        logger.exception("Failed to initialize database")


def save_ticket(state: dict) -> None:
    """Save a support ticket and its final triage results to the database."""
    query = """
    INSERT INTO tickets (
        ticket_id, subject, description, customer_tier,
        category, priority, recommended_team, confidence,
        requires_human_review, reasoning, retrieved_context, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        # Serialize list of context snippets to a JSON string
        retrieved_context_json = json.dumps(state.get("retrieved_context", []))
        
        # Convert bool to int (0 or 1)
        requires_review_int = 1 if state.get("requires_human_review", True) else 0
        
        created_at = datetime.utcnow().isoformat()

        with get_db_connection() as conn:
            conn.execute(
                query,
                (
                    state["ticket_id"],
                    state["subject"],
                    state["description"],
                    state["customer_tier"],
                    state["category"],
                    state["priority"],
                    state["recommended_team"],
                    state["confidence"],
                    requires_review_int,
                    state["reasoning"],
                    retrieved_context_json,
                    created_at,
                )
            )
            conn.commit()
        logger.info("Ticket %s saved to database", state["ticket_id"])
    except Exception:
        logger.exception("Failed to save ticket %s to database", state.get("ticket_id"))


def get_history(limit: int = 10) -> list[dict]:
    """Retrieve recent triage decisions from the database."""
    query = """
    SELECT * FROM tickets
    ORDER BY created_at DESC
    LIMIT ?;
    """
    history = []
    try:
        with get_db_connection() as conn:
            rows = conn.execute(query, (limit,)).fetchall()
            for row in rows:
                history.append({
                    "ticket_id": row["ticket_id"],
                    "subject": row["subject"],
                    "description": row["description"],
                    "customer_tier": row["customer_tier"],
                    "category": row["category"],
                    "priority": row["priority"],
                    "recommended_team": row["recommended_team"],
                    "confidence": row["confidence"],
                    "requires_human_review": bool(row["requires_human_review"]),
                    "reasoning": row["reasoning"],
                    # Deserialize JSON string back to list of snippets
                    "retrieved_context": json.loads(row["retrieved_context"]),
                    "created_at": row["created_at"]
                })
    except Exception:
        logger.exception("Failed to fetch triage history")
    return history
