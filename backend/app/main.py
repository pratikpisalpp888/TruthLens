"""
TruthLens Backend — FastAPI Application Entry Point.
"""

import time
import uuid
import datetime
import structlog
import httpx
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from qdrant_client import AsyncQdrantClient
from minio import Minio

from app.core.config import settings
from app.core.exceptions import TruthLensException
from app.core.logging import configure_logging, request_id_var, request_start_time_var

# API Routers
from app.api.v1 import (
    auth, cases, documents, analysis, analytics,
    settings as settings_router, itr, rag, fraud_dna,
    orchestration, audit, chat, syndicate, documents_annotations
)
from app.api import websocket as ws_router

# Setup Logging
configure_logging()
logger = structlog.get_logger(__name__)

# Track startup time for uptime reporting
_startup_time = time.time()
_service_status: dict = {}


async def verify_database():
    from app.db.session import init_db
    try:
        await init_db()
        _service_status["database"] = "connected"
        logger.info("Service verified: Database (tables auto-created)")
    except Exception as e:
        _service_status["database"] = f"error: {e}"
        logger.error(f"Database connection failed: {e}")
        raise


async def verify_qdrant():
    try:
        from qdrant_client import AsyncQdrantClient
        if settings.QDRANT_MODE.lower() in ("memory", "persistent"):
            _service_status["qdrant"] = f"connected ({settings.QDRANT_MODE})"
            logger.info(f"Service verified: Qdrant ({settings.QDRANT_MODE})")
            return
            
        client = AsyncQdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        await client.get_collections()
        _service_status["qdrant"] = "connected"
        logger.info("Service verified: Qdrant")
    except Exception as e:
        _service_status["qdrant"] = f"error: {e}"
        logger.error(f"Qdrant connection failed: {e}")
        raise


async def verify_storage():
    if settings.STORAGE_TYPE.lower() == "local":
        _service_status["storage"] = "connected (local)"
        import os
        os.makedirs(settings.STORAGE_PATH, exist_ok=True)
        logger.info("Service verified: Local Storage")
        return
        
    client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False
    )
    try:
        import asyncio
        loop = asyncio.get_event_loop()

        def check_and_create():
            if not client.bucket_exists(settings.MINIO_BUCKET):
                client.make_bucket(settings.MINIO_BUCKET)
                logger.info(f"Created MinIO bucket: {settings.MINIO_BUCKET}")
            logger.info("Service verified: MinIO")

        await loop.run_in_executor(None, check_and_create)
        _service_status["storage"] = "connected (minio)"
    except Exception as e:
        _service_status["storage"] = f"unavailable: {e}"
        logger.warning(f"Storage (MinIO) not available — local mode active: {e}")
        # Non-fatal for local dev


async def verify_ollama():
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            response = await client.get(f"{settings.OLLAMA_HOST}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            model_names = [m.get("name") for m in models]
            model_ok = any(settings.OLLAMA_MODEL in n for n in model_names)
            if not model_ok:
                logger.warning(f"Ollama model {settings.OLLAMA_MODEL} not found. Pull with: ollama pull {settings.OLLAMA_MODEL}")
            _service_status["ollama"] = "connected"
            _service_status["model_loaded"] = settings.OLLAMA_MODEL if model_ok else "not_pulled"
            logger.info("Service verified: Ollama")
        except Exception as e:
            _service_status["ollama"] = f"unavailable: {e}"
            logger.warning(f"Ollama not available (AI analysis will be limited): {e}")
            # Non-fatal — continue startup without Ollama


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _startup_time
    _startup_time = time.time()
    logger.info("Starting TruthLens Platform...")

    await verify_database()
    try:
        await verify_qdrant()
    except Exception as e:
        logger.warning(f"Qdrant startup warning (non-fatal): {e}")
    try:
        await verify_storage()
    except Exception as e:
        logger.warning(f"Storage startup warning (non-fatal): {e}")
    await verify_ollama()

    yield
    logger.info("Shutting down TruthLens Platform...")


# ── FastAPI App with full OpenAPI metadata ────────────────────────────────────
app = FastAPI(
    title="TruthLens API",
    description=(
        "**TruthLens** — Production-grade offline AI Document Forensics Platform "
        "for Canara Bank's loan underwriting fraud detection.\n\n"
        "## Features\n"
        "- 📁 Document Upload, OCR & NER\n"
        "- 🔬 Forensic Analysis (ELA, Metadata, Font, Printer Fingerprint)\n"
        "- 🤝 Cross-Document Consistency Engine\n"
        "- 📊 ITR Validation with Tax Computation\n"
        "- 🧬 Fraud DNA & Pattern Matching\n"
        "- 🤖 LangGraph 5-Agent Analysis Pipeline\n"
        "- 📖 CRAG + GraphRAG Knowledge System\n"
        "- 📈 Analytics Dashboard\n\n"
        "## Authentication\n"
        "All endpoints (except `/health`) require a Bearer JWT token via `Authorization: Bearer <token>`."
    ),
    version="1.0.0",
    contact={"name": "Canara Bank IT", "email": "truthlens@canara.bank"},
    license_info={"name": "Internal Use Only"},
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Auth", "description": "Login, token refresh, user management"},
        {"name": "Cases", "description": "Loan case lifecycle management"},
        {"name": "Documents", "description": "Document upload, retrieval, and classification"},
        {"name": "Analysis", "description": "Forensic analysis endpoints"},
        {"name": "ITR", "description": "ITR Special Verification Module"},
        {"name": "Fraud DNA", "description": "Fraud pattern extraction and matching"},
        {"name": "Orchestration", "description": "Full LangGraph pipeline and report generation"},
        {"name": "RAG", "description": "CRAG knowledge base and GraphRAG fraud network"},
        {"name": "Analytics", "description": "Dashboard and trend analytics"},
        {"name": "Settings", "description": "Admin-only system configuration"},
        {"name": "Audit", "description": "Immutable audit log access"},
        {"name": "Health", "description": "System health and status"},
    ]
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request ID Middleware ─────────────────────────────────────────────────────
@app.middleware("http")
async def add_context_middleware(request: Request, call_next):
    req_id = str(uuid.uuid4())
    request_id_var.set(req_id)
    request_start_time_var.set(time.time())
    response = await call_next(request)
    response.headers["X-Request-ID"] = req_id
    return response


# ── Standardized Error Handler ────────────────────────────────────────────────
@app.exception_handler(TruthLensException)
async def custom_exception_handler(request: Request, exc: TruthLensException):
    logger.error("Exception occurred", error_code=exc.error_code, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "error_code": exc.error_code,
            "message": exc.detail,
            "details": {},
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "request_id": request_id_var.get("unknown")
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": str(exc),
            "details": {},
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "request_id": request_id_var.get("unknown")
        }
    )


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(cases.router, prefix="/api/v1", tags=["Cases"])
app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])
app.include_router(documents_annotations.router, prefix="/api/v1", tags=["Documents Annotations"])
app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(itr.router, prefix="/api/v1/itr", tags=["ITR"])
app.include_router(rag.router, prefix="/api/v1", tags=["RAG"])
app.include_router(fraud_dna.router, prefix="/api/v1", tags=["Fraud DNA"])
app.include_router(orchestration.router, prefix="/api/v1", tags=["Orchestration"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(settings_router.router, prefix="/api/v1", tags=["Settings"])
app.include_router(audit.router, prefix="/api/v1", tags=["Audit"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(syndicate.router, prefix="/api/v1", tags=["Syndicate"])
app.include_router(ws_router.router)


# ── Enhanced Health Check ─────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    """Enhanced health check with per-service status."""
    return {
        "status": "healthy",
        "database": _service_status.get("database", "unknown"),
        "qdrant": _service_status.get("qdrant", "unknown"),
        "ollama": _service_status.get("ollama", "unknown"),
        "storage": _service_status.get("storage", "unknown"),
        "jwt": "configured" if settings.JWT_SECRET else "missing",
        "uptime_seconds": round(time.time() - _startup_time),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }


@app.get("/", tags=["Health"])
async def root():
    """Root API info."""
    return {
        "name": "TruthLens API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }
