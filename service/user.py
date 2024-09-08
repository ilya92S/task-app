import string
from dataclasses import dataclass

from random import random, choice

from repository.user import UserRepository
from schema import UserLoginScheme

@dataclass
class UserService:
    user_repository = UserRepository

    def create_user(self, username: str, password: str) -> UserLoginScheme:
        user = self.user_repository.create_uer(username, password)
        return UserLoginScheme(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_access_token() -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))








