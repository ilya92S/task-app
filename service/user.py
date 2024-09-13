from dataclasses import dataclass

from exception import UserExist
from repository import UserRepository
from schema import UserLoginScheme
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginScheme:
        if self.user_repository.get_user_by_username(username=username):
            raise UserExist
        user = self.user_repository.create_user(username=username, password=password)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginScheme(user_id=user.id, access_token=access_token)


