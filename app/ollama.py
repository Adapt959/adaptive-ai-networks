"""Shared non-streaming Ollama transport; configuration stays on the server."""
import os
import httpx
from fastapi import HTTPException

async def call_model(model: str, prompt: str):
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{base_url}/api/chat",
                json={"model": model,
                      "messages": [{"role": "user", "content": prompt}],
                      "stream": False},
            )
            response.raise_for_status()
            result = response.json()
    except httpx.TimeoutException as exc:
        raise HTTPException(504, "Ollama timed out. Try a smaller model or retry.") from exc
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(502, "Ollama model or endpoint not found. Check the installed model name.") from exc
        raise HTTPException(502, "Ollama rejected the request.") from exc
    except httpx.RequestError as exc:
        raise HTTPException(503, "Cannot reach Ollama. Check that it is running and OLLAMA_BASE_URL is correct.") from exc
    except ValueError as exc:
        raise HTTPException(502, "Ollama returned invalid JSON.") from exc
    if not isinstance(result, dict) or result.get("error") or not isinstance(result.get("message"), dict) or not isinstance(result["message"].get("content"), str):
        raise HTTPException(502, "Ollama returned an invalid chat response.")
    return result
