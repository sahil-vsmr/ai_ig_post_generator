from fastapi import APIRouter

from app.api import endpoints

router = APIRouter()
router.include_router(endpoints.health.router)
router.include_router(endpoints.media.router)
router.include_router(endpoints.post.router)
