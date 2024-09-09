from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from dependency import get_auth_service
from exeption import UserNotFoundException, UserNotCorrectPasswordException
from schema import UserLoginScheme, UserCreateSchema
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/login",
    response_model=UserLoginScheme
)
async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )