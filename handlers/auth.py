
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
    print(redirect_url)
    return RedirectResponse(redirect_url)

@router.get(
    "/google"
)
async def google_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    """
    Эта ручка записана в настройках гугла когда я создавал приложение в гугле,
    выглядит она так /auth/google, и на нее происходит редирект после входа с
    помощью гугла, то есть сюда приходит code, по которому мы понимаем что у
    на уже есть такой пользователь, если нет регистрируем записал google_access_token
    """
    print(f"google {code=}")
    return auth_service.google_auth(code=code)


@router.get(
    "/login/yandex",
    response_class=RedirectResponse
)
async def yandex_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)

@router.get(
    "/yandex"
)
async def yandex_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return auth_service.yandex_auth(code=code)
