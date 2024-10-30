from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from os import access

import jwt
from jwt import PyJWTError
from sqlalchemy.util import await_only

from client import GoogleClient, YandexClient
from exception import (
    UserNotCorrectPasswordException,
    UserNotFoundException,
    TokenExpired,
    TokenNotCorrect
)
from models import UserProfile
from repository import UserRepository
from schema import UserLoginScheme, UserCreateScheme
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings()
    google_client: GoogleClient
    yandex_client: YandexClient

    async def login(self, username: str, password: str) -> UserLoginScheme:
        user = await self.user_repository.get_user_by_username(username=username)
        self._validate_auth_user(user, password)
        print(f"наш id {user.id} от пользователя {userт}")
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

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)

            return UserLoginScheme(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateScheme(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)

        return UserLoginScheme(user_id=created_user.id, access_token=access_token)

    def get_yandex_auth(self, code: str):
        print(code)

    async def google_auth(self, code: str):
        """
        Мы должны сходить в гугл по этому коду в гугл
        и получить поределенные данные.
        Здесь мы обращаемся к внешнему сервису, здесь мы
        должны написать клиента, это еще одна дополнительная сущность,
        которая инкапсулирует в себе запросы в другие сервисы, например
        OAuth_client. Клиент будет иметь в себе все методы, которые
        будут иметь авторизацию через другие сервисы. В моем случае
        в папке /client/google.py
        """
        user_data = await self.google_client.get_user_info(code=code)
        # мы получили данные пользователя из аккаунта гугл
        # если в БД есть пользователь с google_token, то не создаем его,
        # иначе создаем.
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print("user login")
            return UserLoginScheme(user_id=user.id, access_token=access_token)

        # если пользователя в БД по гугл токену нет, то
        # записываем в гугл репозиторий
        create_user_data = UserCreateScheme(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        # именно сгенерированный токен отправляем на фронт
        print("user_create")
        return UserLoginScheme(user_id=created_user.id, access_token=access_token)
        # Здесь access_token это не гугловый access_token, он служит только для того
        # что бы пользователь мог связать свою гугловую учотку с той что у нас есть
        # в БД. Если у нас нет учетной записи по гугловому токену, то создаем запись
        # этого пользователя в БД, если есть, то просто связываем или же авторизуем
        # не создавая нового пользователя


    # произошла грубая ошибка гугловский токен не уникален и по нему определять
    # пользователя не стоит, нужно определять по email
