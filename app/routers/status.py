from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["status"])
async def root():
    # Process health only; Ollama may be offline.
    return {"status": "Adaptive AI Backend Running"}
