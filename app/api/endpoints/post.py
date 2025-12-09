from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.services.post_service import generate_post_content, publish_reviewed_post

router = APIRouter()

class PostRequest(BaseModel):
    media_id: Optional[str] = None
    topic: Optional[str] = None
    idea: Optional[str] = None
    tone: Optional[str] = "friendly"
    style: Optional[str] = "short"
    suggestions: Optional[str] = None


class PublishRequest(BaseModel):
    caption: str
    media_url: str
    hashtags: Optional[List[str]] = None
    dry_run: Optional[bool] = False

@router.post("/generate")
def generate_post(request: PostRequest):
    if not any([request.media_id, request.topic, request.idea]):
        # AI ideation mode
        pass
    
    try:
        output = generate_post_content(
            media_id=request.media_id,
            topic=request.topic,
            idea=request.idea,
            tone=request.tone,
            style=request.style,
            suggestions=request.suggestions,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return output


@router.post("/publish")
def publish_post(request: PublishRequest):
    try:
        output = publish_reviewed_post(
            caption=request.caption,
            media_url=request.media_url,
            hashtags=request.hashtags,
            dry_run=request.dry_run or False,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return output
