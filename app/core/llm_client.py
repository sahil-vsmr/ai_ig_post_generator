import json
from typing import Any, Dict

from openai import OpenAI

from app.config import settings


def call_llm(prompt: str) -> Dict[str, Any]:
    """
    Call OpenAI chat completion API and return parsed JSON.
    """
    if not settings.llm_api_key:
        raise RuntimeError("OpenAI API key missing. Set llm_api_key in environment or .env")

    client = OpenAI(api_key=settings.llm_api_key)

    try:
        completion = client.chat.completions.create(
            model=settings.llm_model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Instagram copywriter. "
                        "Respond ONLY with a JSON object that contains the keys: "
                        "hook, caption, cta, hashtags (max 8), carousel_idea, reel_idea."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.7,
            top_p=0.9,
        )
    except Exception as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    content = completion.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"LLM returned non-JSON content: {content}") from exc
