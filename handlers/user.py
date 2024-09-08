from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/login")
async def create_user(user):
    pass