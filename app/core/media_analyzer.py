import base64
from openai import OpenAI
from app.config import settings


def _encode_image(media_path: str) -> str:
    try:
        with open(media_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError as exc:
        raise RuntimeError(f"Media file not found: {media_path}") from exc
    except OSError as exc:
        raise RuntimeError(f"Unable to read media file: {media_path}") from exc


def _vision_prompt() -> str:
    return (
        "You are an expert visual analyst for Instagram.\n"
        "Identify objects, scenes, and environment.\n"
        "Detect emotions, aesthetics, vibe, and inferred intent in the photo.\n"
        "Detect style (minimalistic, artsy, candid, product-style).\n"
        "Offer a concise, human-like natural-language summary of the photo.\n"
        "Spot trends (motivational quote, travel reel, food blog, fitness, desk setup, etc.).\n"
        "Respond with a short paragraph (<= 80 words)."
    )


def analyze_image(media_path: str) -> str:
    """
    Use a multimodal LLM (e.g., GPT-4o) to produce a caption-ready description.
    """
    if not settings.llm_api_key:
        raise RuntimeError("OpenAI API key missing. Set llm_api_key in environment or .env")
    if not settings.llm_model:
        raise RuntimeError("OpenAI model not configured (settings.llm_model).")

    client = OpenAI(api_key=settings.llm_api_key)
    image_b64 = _encode_image(media_path)

    try:
        completion = client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": _vision_prompt()},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                        }
                    ],
                },
            ],
            max_tokens=220,
            temperature=0.4,
            top_p=0.9,
        )
    except Exception as exc:
        raise RuntimeError(f"Vision LLM request failed: {exc}") from exc
    
    content = completion.choices[0].message.content
    print(content)
    if not content:
        raise RuntimeError("Vision LLM returned empty content.")

    return content.strip()
