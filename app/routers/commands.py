import json
import os
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.ollama import call_model

router = APIRouter()

class CommandRequest(BaseModel):
    command: str = Field(min_length=1, pattern=r"\S")
    context: dict | None = None

@router.post("/run")
async def run(body: CommandRequest):
    cmd = body.command.lower()
    if "code" in cmd or "script" in cmd:
        model = os.getenv("OLLAMA_CODE_MODEL", "qwen2.5-coder")
    elif "analyze" in cmd or "reason" in cmd:
        model = os.getenv("OLLAMA_REASON_MODEL", "deepseek-r1")
    else:
        model = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.1")
    prompt = f"Command: {body.command}\nContext: {json.dumps(body.context or {})}"
    result = await call_model(model, prompt)
    return {"selected_model": model, "result": result}
