from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

import jwt

from exception import UserNotCorrectPasswordException, UserNotFoundException
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
