
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException

from dependency import get_user_service
from exception import UserExist
from schema import UserLoginScheme, UserCreateScheme
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])

@router.post("",response_model=UserLoginScheme)
async def create_user(body: UserCreateScheme, user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        return await user_service.create_user(body.username, body.password)
    except UserExist as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
