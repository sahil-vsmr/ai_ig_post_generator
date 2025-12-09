from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.endpoints import health, media, post

app = FastAPI(title="AI Instagram Post Generator - Phase 1")

# Static mounts for the lightweight UI and uploaded files
app.mount("/uploads", StaticFiles(directory="uploaded_media"), name="uploads")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root(request: Request):
    # Basic HTML UI to try the APIs without Postman
    return templates.TemplateResponse("index.html", {"request": request})


# Register endpoints
app.include_router(media.router, prefix="/media", tags=["media"])
app.include_router(post.router, prefix="/post", tags=["post"])
app.include_router(health.router, prefix="/health", tags=["health"])
