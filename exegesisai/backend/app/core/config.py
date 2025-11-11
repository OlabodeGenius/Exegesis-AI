from functools import lru_cache
from pydantic import BaseModel
import os


class Settings(BaseModel):
	env: str = os.getenv("ENV", "dev")
	api_base_url: str = os.getenv("API_BASE_URL", "http://0.0.0.0:8000")
	jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
	jwt_expires_min: int = int(os.getenv("JWT_EXPIRES_MIN", "60"))
	refresh_expires_min: int = int(os.getenv("REFRESH_EXPIRES_MIN", "43200"))

	database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://exegesis:exegesis@db:5432/exegesis")
	redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
	vector_database_url: str = os.getenv("VECTOR_DATABASE_URL", "postgresql+psycopg://exegesis:exegesis@db:5432/exegesis")

	bible_api_provider: str = os.getenv("BIBLE_API_PROVIDER", "esv")
	bible_api_key: str = os.getenv("BIBLE_API_KEY", "your-esv-key")
	openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
	embeddings_provider: str = os.getenv("EMBEDDINGS_PROVIDER", "openai")

	s3_endpoint: str = os.getenv("S3_ENDPOINT", "http://minio:9000")
	s3_bucket: str = os.getenv("S3_BUCKET", "exegesis-exports")
	s3_access_key: str = os.getenv("S3_ACCESS_KEY", "change-me")
	s3_secret_key: str = os.getenv("S3_SECRET_KEY", "change-me")
	s3_region: str = os.getenv("S3_REGION", "auto")

	cors_allow_origins: list[str] = ["*"] if os.getenv("ENV", "dev") == "dev" else [os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")]


@lru_cache
def get_settings() -> Settings:
	return Settings()


settings = get_settings()
*** End Patch  !*** }  QWidget ***!

