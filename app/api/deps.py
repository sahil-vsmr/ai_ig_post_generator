from functools import lru_cache

import boto3
from botocore.client import BaseClient

from app.config import settings
from app.core.llm_client import LLMClient
from app.utils.logger import get_logger

logger = get_logger()


@lru_cache
def get_s3_client() -> BaseClient:
    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
    )


def get_llm_client() -> LLMClient:
    return LLMClient(api_key=settings.llm_api_key, model=settings.llm_model)
