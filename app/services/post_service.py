from app.core.media_analyzer import analyze_image
from app.core.prompt_builder import build_prompt
from app.core.llm_client import call_llm
from app.services.instagram_service import publish_instagram_post
from app.services.media_service import get_media_path

def generate_post_content(
    media_id=None,
    topic=None,
    idea=None,
    tone="friendly",
    style="short",
    suggestions=None,
):
    media_description = None
    if media_id:
        media_path = get_media_path(media_id)
        if not media_path:
            raise RuntimeError(f"Media file not found: {media_id}")
        media_description = analyze_image(media_path)

    prompt = build_prompt(
        media_description=media_description,
        topic=topic,
        idea=idea,
        tone=tone,
        style=style,
        suggestions=suggestions,
    )

    # Call LLM (OpenAI GPT-5, etc.)
    output = call_llm(prompt)
    return output


def publish_reviewed_post(caption: str, media_url: str, hashtags=None, dry_run: bool = False):
    """
    Publish the reviewed content to Instagram using the Graph API.
    """
    if not caption:
        raise ValueError("caption is required")
    if not media_url:
        raise ValueError("media_url is required for Instagram publishing")

    return publish_instagram_post(
        caption=caption,
        media_url=media_url,
        hashtags=hashtags,
        dry_run=dry_run,
    )
