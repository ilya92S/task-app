from dataclasses import dataclass

from fastapi import HTTPException, status

@dataclass
class UserNotFoundException(HTTPException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Пользователь не найден"

@dataclass
class UserNotCorrectPasswordException(HTTPException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Пароль не верный"
