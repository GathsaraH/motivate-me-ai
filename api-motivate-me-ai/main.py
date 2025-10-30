from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading .env...")
load_dotenv()
api_key_from_env = os.getenv("OPENAI_API_KEY")
if not api_key_from_env:
    print("[LOG] OPENAI_API_KEY not found in environment variables!")
else:
    print(f"[LOG] OPENAI_API_KEY loaded: {{masked}} {api_key_from_env[:5]}...{api_key_from_env[-5:]}")
openai.api_key = api_key_from_env

class ThemeRequest(BaseModel):
    theme: str

@app.post("/generate")
async def generate_quote(request: ThemeRequest):
    print(f"[LOG] Incoming theme: {request.theme}")
    if not openai.api_key:
        print("[LOG] openai.api_key is not set in /generate!")
        raise HTTPException(status_code=500, detail="OpenAI API key not set.")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates motivational quotes."},
                {"role": "user", "content": f"Give me a motivational quote about {request.theme}."},
            ],
            max_tokens=50,
        )
        quote = response.choices[0].message.content.strip()
        print(f"[LOG] Response: {quote}")
        return {"quote": quote}
    except Exception as e:
        print(f"[LOG] OpenAI Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))
