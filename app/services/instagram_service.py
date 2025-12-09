import re
from typing import Any, Dict, List, Optional

import requests

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger()


class InstagramConfigError(RuntimeError):
    """Raised when required Instagram settings are missing."""


class InstagramAPIError(RuntimeError):
    """Raised when the Instagram Graph API returns an error."""


def _require_settings():
    if not settings.instagram_publish_enabled:
        raise InstagramConfigError("Instagram publishing disabled. Set instagram_publish_enabled=True.")
    if not settings.instagram_access_token:
        raise InstagramConfigError("instagram_access_token is not configured.")
    if not settings.instagram_user_id:
        raise InstagramConfigError("instagram_user_id is not configured.")


def _normalize_hashtags(hashtags: Optional[List[str]]) -> str:
    if not hashtags:
        return ""
    cleaned = []
    for tag in hashtags:
        if not tag:
            continue
        tag = tag.strip()
        if not tag:
            continue
        if not tag.startswith("#"):
            tag = f"#{tag}"
        cleaned.append(re.sub(r"\s+", "", tag))
    return " ".join(cleaned)


def _build_caption(caption: str, hashtags: Optional[List[str]]) -> str:
    caption = caption.strip()
    tag_block = _normalize_hashtags(hashtags)
    if tag_block:
        return f"{caption}\n\n{tag_block}"
    return caption


def _post(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        resp = requests.post(url, params=params, timeout=15)
    except requests.RequestException as exc:
        raise InstagramAPIError(f"Network error calling Instagram API: {exc}") from exc

    try:
        payload = resp.json()
    except ValueError:
        raise InstagramAPIError(f"Non-JSON response from Instagram API: {resp.text}")

    if not resp.ok:
        raise InstagramAPIError(f"Instagram API error: {payload}")
    if "error" in payload:
        raise InstagramAPIError(f"Instagram API returned error: {payload['error']}")
    return payload


def publish_instagram_post(
    caption: str,
    media_url: str,
    hashtags: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Create and publish a single-image Instagram post using the Graph API.

    Args:
        caption: The reviewed caption text.
        media_url: Publicly accessible URL of the image to post.
        hashtags: Optional list of hashtags; "#" will be added if missing.
        dry_run: If True, skip publish call and return the creation payload.
    """
    _require_settings()

    if not media_url:
        raise ValueError("media_url is required and must be publicly accessible.")

    full_caption = _build_caption(caption, hashtags)
    base_url = settings.instagram_graph_base_url.rstrip("/")

    logger.info("Creating Instagram media container", extra={"media_url": media_url})
    creation_payload = _post(
        f"{base_url}/{settings.instagram_user_id}/media",
        params={
            "image_url": media_url,
            "caption": full_caption,
            "access_token": settings.instagram_access_token,
        },
    )

    creation_id = creation_payload.get("id")
    if not creation_id:
        raise InstagramAPIError(f"Missing creation id in response: {creation_payload}")

    if dry_run:
        return {
            "status": "container_created",
            "dry_run": True,
            "creation_id": creation_id,
            "creation_payload": creation_payload,
        }

    logger.info("Publishing Instagram media", extra={"creation_id": creation_id})
    publish_payload = _post(
        f"{base_url}/{settings.instagram_user_id}/media_publish",
        params={
            "creation_id": creation_id,
            "access_token": settings.instagram_access_token,
        },
    )

    publish_id = publish_payload.get("id")
    if not publish_id:
        raise InstagramAPIError(f"Missing publish id in response: {publish_payload}")

    return {
        "status": "published",
        "creation_id": creation_id,
        "publish_id": publish_id,
        "publish_payload": publish_payload,
    }

