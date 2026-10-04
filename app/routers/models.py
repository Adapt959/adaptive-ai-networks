from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.ollama import call_model

router = APIRouter()

class ChatRequest(BaseModel):
    model: str = Field(min_length=1, pattern=r"\S")
    prompt: str = Field(min_length=1, pattern=r"\S")

@router.post("/chat")
async def chat(body: ChatRequest):
    return await call_model(body.model, body.prompt)
