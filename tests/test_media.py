import pytest
from fastapi import UploadFile
from io import BytesIO

from app.services.media_service import MediaService


class DummyS3Client:
    def put_object(self, **kwargs):
        return {"ok": True}


def test_media_upload_creates_key_and_url(event_loop):
    service = MediaService(DummyS3Client())
    file = UploadFile(filename="test.jpg", file=BytesIO(b"data"))
    result = event_loop.run_until_complete(service.upload_media(file))
    assert "key" in result
    assert result["url"].startswith("s3://")
