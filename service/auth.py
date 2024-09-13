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
    def _validate_auth_user(user: UserProfile, password: str):
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
