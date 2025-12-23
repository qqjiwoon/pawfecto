# ai/services/verification.py

import json
import base64
from io import BytesIO
from openai import OpenAI
from django.conf import settings
from PIL import Image


client = OpenAI(
    api_key=settings.GMS_API_KEY,
    base_url=settings.GMS_OPENAI_BASE_URL,
)


def run_ai_verification(prompt: str, images=None):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
            ],
        }
    ]

    # ✅ 테스트용 public 이미지 URL
    messages[0]["content"].append(
        {
            "type": "image_url",
            "image_url": {
                "url": "https://images.unsplash.com/photo-1558788353-f76d92427f16"
            },
        }
    )

    response = client.chat.completions.create(
        model=settings.AI_MODEL_PRIMARY,
        messages=messages,
        temperature=1,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1].strip()
        if raw.startswith("json"):
            raw = raw[4:].strip()

    return json.loads(raw)
