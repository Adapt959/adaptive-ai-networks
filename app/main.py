from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import commands, models, status

app = FastAPI(title="Adaptive AI Local Command Center")
app.include_router(status.router)
app.include_router(models.router, prefix="/models", tags=["models"])
app.include_router(commands.router, prefix="/commands", tags=["commands"])

_DESK_HTML = Path(__file__).parent / "static" / "lead_desk.html"


@app.get("/desk", response_class=HTMLResponse, include_in_schema=False)
def lead_desk():
    """One-screen JARVIS lead desk: lead details -> draft -> review -> approve -> copy."""
    return _DESK_HTML.read_text(encoding="utf-8")
