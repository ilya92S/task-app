from fastapi import APIRouter

from settings import settings

router = APIRouter(prefix="/ping", tags=["ping"])

@router.get("/db")
async def ping_db():
    token = settings.GOOGLE_TOKEN_ID
    return {"token": token}

@router.get("/app")
async def ping_app():
    return {"text": "app is working"}