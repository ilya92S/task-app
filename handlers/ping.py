from fastapi import APIRouter

from settings import Settings

router = APIRouter(prefix="/ping", tags=["ping"])

settings = Settings()

@router.get("/db")
async def ping_db():
    token = settings.GOOGLE_TOKEN_ID
    return {"token": token}

@router.get("/app")
async def ping_app():
    return {"text": "app is working"}