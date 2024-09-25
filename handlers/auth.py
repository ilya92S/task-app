
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import RedirectResponse

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

@router.get(
    "/login/google",
    response_class=RedirectResponse
)
async def google_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    """
    Пользователь переходит по /login/google, редиректится на
    страницу с авторизацией через гугл, и гугл нам отправляет
    запрос с кодом в нашу ручку с кодом, которая будет ниже.
    """
    redirect_url = auth_service.get_google_redirect_url()
    return RedirectResponse(redirect_url)

@router.get(
    "/auth/google"
)
async def google_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return auth_service.google_auth(code=code)
