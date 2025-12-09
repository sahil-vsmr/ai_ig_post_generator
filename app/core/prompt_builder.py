def build_prompt(
    media_description=None,
    topic=None,
    idea=None,
    tone="friendly",
    style="short",
    suggestions=None,
):
    prompt = "You are an expert Instagram copywriter.\n"
    if media_description:
        prompt += f"Media Description: {media_description}\n"
    if topic:
        prompt += f"Topic: {topic}\n"
    if idea:
        prompt += f"Idea: {idea}\n"
    prompt += f"Tone: {tone}\nStyle: {style}\n"
    if suggestions:
        prompt += (
            "User suggestions to incorporate:\n"
            f"{suggestions}\n"
            "Respect these requests while keeping the copy concise and Instagram-ready.\n"
        )
    prompt += (
        "Return ONLY a JSON object with keys: "
        "hook, caption, cta, hashtags (max 8), carousel_idea, reel_idea. "
        "Do not include any additional text, explanations, or formatting."
    )
    return prompt
