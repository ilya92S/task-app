from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

import jwt
from jwt import PyJWTError

from exception import (
    UserNotCorrectPasswordException,
    UserNotFoundException,
    TokenExpired,
    TokenNotCorrect
)
from models import UserProfile
from repository import UserRepository
from schema import UserLoginScheme
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings()

    def login(self, username: str, password: str) -> UserLoginScheme:
        user = self.user_repository.get_user_by_username(username=username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginScheme(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expire = (datetime.now(timezone.utc) + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "expire": expire},
            key=self.settings.SECRET_KEY,
            algorithm=self.settings.ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token,
                key=self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM]
            )
        except PyJWTError:
            raise TokenNotCorrect
        if payload["expire"] < datetime.now(timezone.utc).timestamp():
            raise TokenExpired
        return payload["user_id"]

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def google_auth(self, code: str):
        """
        Мы должны сходить в гугл по этому коду в гугл
        и получить поределенные данные.
        Здесь мы обращаемся к внешнему сервису, здесь мы
        должны написать клиента, это еще одна дополнительная сущность,
        которая инкапсулирует в себе запросы в другие сервисы, например
        OAuth_client. Клиент будет иметь в себе все методы, которые
        будут иметь авторизацию через другие сервисы. В моем случае
        в папке /client/google_client.py
        """
        pass
