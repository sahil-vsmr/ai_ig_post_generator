from pydantic import BaseModel

class MediaResponse(BaseModel):
    media_id: str
    url: str
    status: str
