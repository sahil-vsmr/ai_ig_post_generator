from pydantic import BaseModel, Field


class PostGenerateRequest(BaseModel):
    topic: str | None = Field(None, description="Topic for the post")
    tone: str | None = Field(None, description="Desired tone, e.g., friendly, professional")
    media_key: str | None = Field(None, description="S3 key for uploaded media")


class PostGenerateResponse(BaseModel):
    caption: str
    hashtags: list[str]
