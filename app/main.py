from fastapi import FastAPI
from app.routers import commands, models, status

app = FastAPI(title="Adaptive AI Local Command Center")
app.include_router(status.router)
app.include_router(models.router, prefix="/models", tags=["models"])
app.include_router(commands.router, prefix="/commands", tags=["commands"])
