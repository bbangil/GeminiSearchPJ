from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("사용가능한모델목록:")
for m in client.models.list():
	print(f"- {m.name}")
