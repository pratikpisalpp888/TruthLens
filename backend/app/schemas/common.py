"""
TruthLens — Common Pydantic Schemas.

Shared schema components used across multiple domain schemas.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

DataT = TypeVar("DataT")


class TruthLensBaseModel(BaseModel):
    """
    Base Pydantic model for all TruthLens schemas.

    Configures:
    - ORM mode for SQLAlchemy model serialization
    - Strict string stripping
    - Population by field name
    """

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class PaginatedResponse(TruthLensBaseModel, Generic[DataT]):
    """
    Generic paginated response wrapper.

    Wraps a list of items with pagination metadata.
    """

    items: list[DataT] = Field(description="Page of result items")
    total: int = Field(description="Total count of matching records")
    page: int = Field(description="Current page number (1-indexed)")
    page_size: int = Field(description="Number of items per page")
    pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether a next page exists")
    has_prev: bool = Field(description="Whether a previous page exists")

    @classmethod
    def create(
        cls,
        items: list[Any],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse":
        """Build a paginated response from raw data."""
        pages = max(1, (total + page_size - 1) // page_size)
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )


class SuccessResponse(TruthLensBaseModel):
    """Standard success response for non-data operations."""

    success: bool = True
    message: str = "Operation completed successfully."


class ErrorResponse(TruthLensBaseModel):
    """Standard error response schema."""

    error: str = Field(description="Machine-readable error code")
    message: str = Field(description="Human-readable error message")
    detail: Any | None = Field(default=None, description="Additional error context")


class HealthStatus(TruthLensBaseModel):
    """Individual service health status."""

    status: str = Field(description="Service status: healthy|unhealthy|degraded")
    backend: str | None = None
    model: str | None = None
    error: str | None = None


class HealthCheckResponse(TruthLensBaseModel):
    """Platform-wide health check response."""

    status: str
    version: str
    environment: str
    timestamp: str
    services: dict[str, HealthStatus]
