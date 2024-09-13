
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException

from dependency import get_auth_service
from exception import UserNotFoundException, UserNotCorrectPasswordException
from schema import UserLoginScheme, UserCreateScheme
from service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=UserLoginScheme
)
async def login(
    body: UserCreateScheme,
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

