from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TokenIsNotExistException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен не существует"


class UserAlreadyExistException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class UserIsNotAuthenticatedException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не верный адрес почты или пароль"


class InvalidTokenFormatException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не верный формат токена"


class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Истёк срок действия токена"


class DataAboutUserIsNotExistException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Нет данных о пользователе"


class WrongDataAboutUserException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверные данные о пользователе"


class UserIsNotExistException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Пользователь не существует"
