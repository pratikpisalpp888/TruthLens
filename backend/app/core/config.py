"""
TruthLens — Application Configuration.

Centralized settings management using Pydantic v2 BaseSettings.
Loads variables from .env file.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Database Setup
    DATABASE_URL: str = Field(default="postgresql+asyncpg://truthlens:truthlens123@localhost:5432/truthlens", description="Database connection URL")
    DATABASE_ECHO: bool = Field(default=False, description="Log SQL queries")
    DATABASE_POOL_SIZE: int = Field(default=10, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Database connection max overflow")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, description="Database connection pool timeout")
    # Qdrant Vector DB Setup
    QDRANT_HOST: str = Field(default="localhost", description="Qdrant host name")
    QDRANT_PORT: int = Field(default=6333, description="Qdrant REST port")
    QDRANT_MODE: str = Field(default="persistent", description="Qdrant mode: persistent or memory")
    QDRANT_PATH: str = Field(default="./qdrant_data", description="Path for Qdrant persistent storage")
    
    # File Storage
    STORAGE_TYPE: str = Field(default="local", description="Storage type: local or minio")
    STORAGE_PATH: str = Field(default="./storage", description="Path for local storage")
    MAX_UPLOAD_SIZE_BYTES: int = Field(default=50 * 1024 * 1024, description="Max upload size in bytes")
    
    # MinIO Config
    MINIO_ENDPOINT: str = Field(default="localhost:9000", description="MinIO endpoint (host:port)")
    MINIO_ACCESS_KEY: str = Field(default="truthlens", description="MinIO root access key")
    MINIO_SECRET_KEY: str = Field(default="truthlens123", description="MinIO root secret key")
    MINIO_BUCKET: str = Field(default="documents", description="Primary document bucket")
    
    # Ollama
    OLLAMA_HOST: str = Field(default="http://localhost:11434", description="Ollama API host")
    OLLAMA_MODEL: str = Field(default="llama3.1:8b", description="Ollama model to use")
    OLLAMA_TIMEOUT: int = Field(default=120, description="Ollama timeout in seconds")
    OLLAMA_MAX_TOKENS: int = Field(default=2048, description="Max tokens for Ollama")
    OLLAMA_TEMPERATURE: float = Field(default=0.1, description="Temperature for Ollama")
    OLLAMA_TOP_P: float = Field(default=0.9, description="Top p for Ollama")
    OLLAMA_CONTEXT_WINDOW: int = Field(default=4096, description="Context window for Ollama")
    
    # JWT Authentication
    JWT_SECRET: str = Field(default="your-super-secret-key-change-in-production-min-32-chars", description="Secret key for JWT generation")
    JWT_ALGORITHM: str = Field(default="HS256", description="Algorithm for JWT")
    JWT_EXPIRY_MINUTES: int = Field(default=480, description="Token expiration in minutes")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=480, description="Token expiration in minutes")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token expiration in days")
    
    LOG_LEVEL: str = Field(default="INFO", description="Application log level")
    ENCRYPTION_KEY: str = Field(default="0123456789abcdef0123456789abcdef", description="Secret key for AES encryption")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

