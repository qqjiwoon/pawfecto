from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.GMS_API_KEY,
    base_url=settings.GMS_OPENAI_BASE_URL,
)

def call_llm(messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
    )
    return response.choices[0].message.content
