from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.media_service import save_image
from app.models.media import MediaResponse

router = APIRouter()

@router.post("/upload", response_model=MediaResponse)
async def upload_media(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only jpg, png, webp allowed.")
    
    try:
        media_id, url = await save_image(file)
    except Exception as exc:
        # Return structured error instead of plain text so clients don't choke on non-JSON.
        raise HTTPException(status_code=500, detail=str(exc))

    return MediaResponse(media_id=media_id, url=url, status="uploaded")
