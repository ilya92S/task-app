from dataclasses import dataclass

from schema import UserLoginScheme

@dataclass
class AuthService:

    def login(self, username: str, password: str) -> UserLoginScheme:
        pass