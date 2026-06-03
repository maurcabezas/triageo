"""
Triageo FastAPI application entry point.
"""

import logging

# Route our app loggers through uvicorn so they appear in docker logs
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s - %(message)s")

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
from app.api.triage import router as triage_router
from app.services.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the SQLite database schema
    init_db()
    yield

app = FastAPI(
    title="Triageo API",
    description=(
        "Support ticket triage service. "
        "Classifies incoming tickets and routes them to the appropriate team."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — permissive for local dev; tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formats 422 schema validation errors into a cleaner structure."""
    details = exc.errors()
    error_msgs = []
    for err in details:
        loc_path = ".".join(str(l) for l in err['loc'][1:])
        error_msgs.append(f"Field '{loc_path}': {err.get('msg', 'invalid value')}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation Failed",
            "errors": error_msgs
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all for internal server errors to mask debug stacktraces from users."""
    logging.exception("Unhandled application server error occurred")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "message": "An unexpected error occurred during processing. Please contact support or check server logs."
        }
    )


@app.get("/health", tags=["ops"], summary="Health check")
def health() -> dict:
    """Returns service status. Used by Docker and load balancers."""
    return {"status": "ok", "service": "triageo-api", "version": app.version}
