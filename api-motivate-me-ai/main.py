from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class ThemeRequest(BaseModel):
    theme: str

@app.post("/generate")
async def generate_quote(request: ThemeRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not set.")
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Give me a motivational quote about {request.theme}.",
            max_tokens=50,
            n=1
        )
        quote = response.choices[0].text.strip()
        return {"quote": quote}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
