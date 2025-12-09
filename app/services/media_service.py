import os
import uuid
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile

from app.config import settings

# Store uploaded files under repo_root/uploaded_media (local fallback)
MEDIA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploaded_media"))
os.makedirs(MEDIA_DIR, exist_ok=True)


def _s3_bucket() -> Optional[str]:
    return settings.s3_bucket or settings.s3_bucket_name or os.environ.get("S3_BUCKET")


def _public_s3_url(bucket: str, key: str) -> str:
    region = settings.aws_region or os.environ.get("AWS_REGION") or "us-east-1"
    if region == "us-east-1":
        return f"https://{bucket}.s3.amazonaws.com/{key}"
    return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"


async def save_image(file: UploadFile):
    """
    Save an uploaded image to S3 if configured; otherwise fall back to local disk.
    Returns media_id and a URL suitable for Instagram fetch.
    """
    media_id = f"med_{uuid.uuid4().hex[:8]}"
    extension = file.filename.split(".")[-1]
    content_type = file.content_type or "application/octet-stream"
    content = await file.read()

    bucket = _s3_bucket()
    if bucket:
        key = f"uploads/{media_id}.{extension}"
        client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        try:
            client.put_object(Bucket=bucket, Key=key, Body=content, ContentType=content_type)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(f"S3 upload failed: {exc}") from exc
        url = _public_s3_url(bucket, key)
        # Also persist locally so downstream vision analysis can read the file path.
        file_path = os.path.join(MEDIA_DIR, f"{media_id}.{extension}")
        with open(file_path, "wb") as f:
            f.write(content)
        return media_id, url

    # Local fallback (not IG-friendly unless exposed publicly)
    file_path = os.path.join(MEDIA_DIR, f"{media_id}.{extension}")
    with open(file_path, "wb") as f:
        f.write(content)
    url = file_path
    return media_id, url


def get_media_path(media_id: str) -> Optional[str]:
    """
    Resolve a media_id to the stored local file path (with extension).
    """
    for filename in os.listdir(MEDIA_DIR):
        if filename.startswith(media_id + "."):
            return os.path.join(MEDIA_DIR, filename)
    return None
