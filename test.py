from google import genai
from config import settings

if not settings.google_api_key:
    raise RuntimeError("GOOGLE_API_KEY is not configured.")

client = genai.Client(api_key=settings.google_api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text)
