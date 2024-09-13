from fastapi import status


class UserNotFoundException(Exception):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не зарегистрирован"

class UserNotCorrectPasswordException(Exception):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Не корректный пароль"

class UserExist(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Выберите другой username"

class TokenExpired(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "access_token истек"

class TokenNotCorrect(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "access_token не верный"

class TaskNotFound(Exception):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Задача не найдена"
