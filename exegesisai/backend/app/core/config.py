from functools import lru_cache
import os
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application configuration sourced from environment variables."""

    env: str = Field(default_factory=lambda: os.getenv("ENV", "dev"))
    api_base_url: str = Field(default_factory=lambda: os.getenv("API_BASE_URL", "http://0.0.0.0:8000"))
    jwt_secret: str = Field(default_factory=lambda: os.getenv("JWT_SECRET", "change-me"))
    jwt_expires_min: int = Field(default_factory=lambda: int(os.getenv("JWT_EXPIRES_MIN", "60")))
    refresh_expires_min: int = Field(default_factory=lambda: int(os.getenv("REFRESH_EXPIRES_MIN", "43200")))

    database_url: str = Field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://exegesis:exegesis@db:5432/exegesis",
        )
    )
    redis_url: str = Field(default_factory=lambda: os.getenv("REDIS_URL", "redis://redis:6379/0"))
    vector_database_url: str = Field(
        default_factory=lambda: os.getenv(
            "VECTOR_DATABASE_URL",
            "postgresql+psycopg://exegesis:exegesis@db:5432/exegesis",
        )
    )

    bible_api_provider: str = Field(default_factory=lambda: os.getenv("BIBLE_API_PROVIDER", "esv"))
    bible_api_key: str = Field(default_factory=lambda: os.getenv("BIBLE_API_KEY", "your-esv-key"))
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    embeddings_provider: str = Field(default_factory=lambda: os.getenv("EMBEDDINGS_PROVIDER", "openai"))

    s3_endpoint: str = Field(default_factory=lambda: os.getenv("S3_ENDPOINT", "http://minio:9000"))
    s3_bucket: str = Field(default_factory=lambda: os.getenv("S3_BUCKET", "exegesis-exports"))
    s3_access_key: str = Field(default_factory=lambda: os.getenv("S3_ACCESS_KEY", "change-me"))
    s3_secret_key: str = Field(default_factory=lambda: os.getenv("S3_SECRET_KEY", "change-me"))
    s3_region: str = Field(default_factory=lambda: os.getenv("S3_REGION", "auto"))

    frontend_origin: str = Field(default_factory=lambda: os.getenv("FRONTEND_ORIGIN", "http://localhost:3000"))

    @property
    def cors_allow_origins(self) -> List[str]:
        if self.env == "dev":
            return ["*"]
        return [self.frontend_origin] if self.frontend_origin else []


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
