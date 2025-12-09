import os
import uuid
from typing import Optional

from app.utils.logger import get_logger

logger = get_logger()


def generate_key(filename: str) -> str:
    ext = os.path.splitext(filename)[1]
    return f"uploads/{uuid.uuid4()}{ext}"


def upload_bytes(client, data: bytes, key: str, content_type: Optional[str] = None) -> str:
    logger.debug("Uploading to S3", extra={"key": key})
    client.put_object(Bucket=os.environ.get("S3_BUCKET", ""), Key=key, Body=data, ContentType=content_type)
    return f"s3://{os.environ.get('S3_BUCKET', '')}/{key}"
