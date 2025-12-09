import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_region: str | None = None
    s3_bucket_name: str | None = None
    s3_bucket: str | None = None  # alias-friendly for env S3_BUCKET
    # OpenAI
    llm_api_key: str | None = None
    llm_model: str = "gpt-3.5-turbo"
    # Hugging Face Inference API (unused by default)
    hf_api_key: str | None = None
    hf_model: str = "meta-llama/Llama-3.2-3B-Instruct"
    # Instagram Graph API
    instagram_access_token: str | None = None
    instagram_user_id: str | None = None
    instagram_graph_base_url: str = "https://graph.facebook.com/v21.0"
    instagram_publish_enabled: bool = False

    model_config = SettingsConfigDict(
        # Load .env file if it exists (for local development)
        # Environment variables always take precedence
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        case_sensitive=False,
    )

    @field_validator("llm_api_key", mode="before")
    @classmethod
    def get_llm_api_key_from_env(cls, v):
        # Explicitly check environment variable if not set from .env or field
        # This ensures Railway environment variables are always read
        if v:
            return v
        return os.getenv("LLM_API_KEY")


settings = Settings()
