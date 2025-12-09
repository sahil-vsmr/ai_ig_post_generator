import pytest

from app.services.post_service import PostService
from app.models.post import PostGenerateRequest


class DummyLLM:
    async def generate(self, prompt: str):
        return {"text": "Hello IG", "prompt": prompt}


def test_generate_post_returns_caption_and_hashtags(event_loop):
    service = PostService(DummyLLM())
    payload = PostGenerateRequest(topic="travel", tone="fun")
    result = event_loop.run_until_complete(service.generate_post(payload))
    assert result.caption == "Hello IG"
    assert len(result.hashtags) > 0
