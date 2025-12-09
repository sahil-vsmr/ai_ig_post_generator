# AI Instagram Post Generator (MVP)

FastAPI-based service to upload media, analyze it, and generate Instagram-ready captions and hashtags using an LLM.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints
- `GET /health` – Health check
- `POST /media/upload` – Upload media to S3 (returns a public URL)
- `POST /post/generate` – Generate caption + hashtags
- `POST /post/publish` – Publish reviewed caption + image to Instagram Graph API (requires public image URL)

## Environment
Configure `.env` (never commit secrets):
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET=
LLM_API_KEY=
LLM_MODEL=gpt-4o-mini
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_USER_ID=
INSTAGRAM_PUBLISH_ENABLED=false
INSTAGRAM_GRAPH_BASE_URL=https://graph.facebook.com/v21.0
```
