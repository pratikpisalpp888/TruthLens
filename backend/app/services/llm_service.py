"""
TruthLens — LLM Service (Ollama + Phi-3 Mini).

Manages all interactions with the local Ollama inference server.
Provides structured prompt templates for forensic analysis tasks.
"""

from __future__ import annotations

import asyncio
from typing import Any, AsyncGenerator

import httpx
import structlog

from app.core.config import settings
from app.core.exceptions import LLMError, LLMTimeoutError

logger = structlog.get_logger(__name__)


class LLMService:
    """
    Async service for Ollama LLM inference (Phi-3 Mini 3.8B).

    Provides:
    - Chat completion (async)
    - Streaming generation
    - Structured JSON output
    - Forensic-specific prompt templates
    - Health check
    """

    # System prompts for different forensic tasks
    SYSTEM_PROMPTS = {
        "forensic_analyst": (
            "You are an expert forensic document analyst for Canara Bank's loan fraud detection unit. "
            "Your role is to analyze documents for signs of tampering, forgery, or manipulation. "
            "Be precise, factual, and cite specific evidence. Always structure your response as JSON. "
            "Never make assumptions beyond the data provided. Flag suspicious elements clearly."
        ),
        "cross_reference": (
            "You are a cross-document verification specialist. Analyze multiple financial documents "
            "for consistency, looking for discrepancies in names, dates, amounts, and signatures. "
            "Report findings as structured JSON with specific field-level comparisons."
        ),
        "compliance": (
            "You are a banking compliance expert specializing in RBI guidelines and KYC norms. "
            "Review documents for regulatory compliance issues and flag any violations. "
            "Provide actionable recommendations in structured JSON format."
        ),
        "decision": (
            "You are a senior loan underwriting AI assistant. Based on the forensic analysis "
            "provided, generate a clear recommendation (approve/reject/escalate) with detailed "
            "justification. Your response must be in JSON format with a risk_score (0.0-1.0)."
        ),
        "rag": (
            "You are a knowledgeable banking document assistant. Answer questions about documents "
            "based strictly on the provided context. Do not hallucinate. If information is not "
            "in the context, say so explicitly."
        ),
        "itr_extractor": (
            "You are a specialized AI data extraction agent for Indian Income Tax Returns (ITR). "
            "Your job is to read raw, noisy OCR text and accurately extract the following fields into a STRICT JSON object: "
            "'pan' (10-char string), 'acknowledgement_number' (15-digit string), 'assessment_year' (e.g. 2023-24), "
            "'form_type' (e.g. ITR-1), 'name' (string), 'gross_total_income' (float), 'tax_payable' (float), 'deductions_80c' (float). "
            "If a value is truly missing or unreadable, return null or 0.0 for numbers. Do not include any extra text."
        ),
    }

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None
        self._is_ready: bool = False

    async def initialize(self) -> None:
        """
        Initialize the HTTP client and verify Ollama connectivity.

        Raises:
            LLMError: If Ollama is unreachable or model is not available.
        """
        self._client = httpx.AsyncClient(
            base_url=settings.OLLAMA_HOST,
            timeout=httpx.Timeout(settings.OLLAMA_TIMEOUT),
        )
        await self.health_check()
        self._is_ready = True
        logger.info("llm.initialized", model=settings.OLLAMA_MODEL)

    async def health_check(self) -> bool:
        """
        Check if Ollama server is responsive and model is loaded.

        Returns:
            True if healthy.

        Raises:
            LLMError: If the service is unavailable.
        """
        try:
            response = await self._client.get("/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            logger.debug("llm.health_check", models=model_names)
            return True
        except Exception as exc:
            raise LLMError(
                message=f"Ollama server unreachable: {exc}",
                detail=str(exc),
            ) from exc

    async def generate(
        self,
        prompt: str,
        system: str = "forensic_analyst",
        temperature: float | None = None,
        max_tokens: int | None = None,
        json_mode: bool = False,
    ) -> str:
        """
        Generate a completion from the LLM.

        Args:
            prompt: The user prompt.
            system: System prompt key or raw system prompt string.
            temperature: Optional override for temperature.
            max_tokens: Optional max token limit override.
            json_mode: If True, request JSON-formatted output.

        Returns:
            Generated text response.

        Raises:
            LLMTimeoutError: If generation exceeds timeout.
            LLMError: If generation fails.
        """
        system_prompt = self.SYSTEM_PROMPTS.get(system, system)

        payload: dict[str, Any] = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": temperature or settings.OLLAMA_TEMPERATURE,
                "top_p": settings.OLLAMA_TOP_P,
                "num_predict": max_tokens or settings.OLLAMA_MAX_TOKENS,
                "num_ctx": settings.OLLAMA_CONTEXT_WINDOW,
            },
        }

        if json_mode:
            payload["format"] = "json"

        try:
            response = await self._client.post("/api/generate", json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError(
                message=f"LLM generation timed out after {settings.OLLAMA_TIMEOUT}s"
            ) from exc
        except Exception as exc:
            raise LLMError(message=f"LLM generation failed: {exc}", detail=str(exc)) from exc

    async def generate_json(
        self,
        prompt: str,
        system: str = "forensic_analyst",
        temperature: float | None = None,
    ) -> dict[str, Any]:
        """
        Generate a JSON-structured response from the LLM.

        Automatically enables JSON mode and parses the response.

        Args:
            prompt: The user prompt.
            system: System prompt key or raw string.
            temperature: Optional temperature override.

        Returns:
            Parsed JSON response dictionary.

        Raises:
            LLMError: If response is not valid JSON.
        """
        import json

        raw = await self.generate(
            prompt=prompt,
            system=system,
            temperature=temperature,
            json_mode=True,
        )

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.warning("llm.json_parse_failed", raw=raw[:200])
            raise LLMError(
                message="LLM returned invalid JSON.",
                detail={"raw_response": raw[:500]},
            ) from exc

    async def chat(
        self,
        messages: list[dict[str, str]],
        system: str | None = None,
        temperature: float | None = None,
    ) -> str:
        """
        Multi-turn chat completion.

        Args:
            messages: List of {"role": "user"|"assistant", "content": "..."}.
            system: Optional system prompt override.
            temperature: Optional temperature override.

        Returns:
            Assistant's response text.
        """
        system_prompt = (
            self.SYSTEM_PROMPTS.get(system, system)
            if system
            else self.SYSTEM_PROMPTS["forensic_analyst"]
        )

        payload: dict[str, Any] = {
            "model": settings.OLLAMA_MODEL,
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "stream": False,
            "options": {
                "temperature": temperature or settings.OLLAMA_TEMPERATURE,
                "top_p": settings.OLLAMA_TOP_P,
                "num_predict": settings.OLLAMA_MAX_TOKENS,
                "num_ctx": settings.OLLAMA_CONTEXT_WINDOW,
            },
        }

        try:
            response = await self._client.post("/api/chat", json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("message", {}).get("content", "")
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError() from exc
        except Exception as exc:
            raise LLMError(message=str(exc)) from exc

    async def close(self) -> None:
        """Close the HTTP client connection pool."""
        if self._client:
            await self._client.aclose()

    @property
    def is_ready(self) -> bool:
        """Return True if the service is initialized."""
        return self._is_ready
