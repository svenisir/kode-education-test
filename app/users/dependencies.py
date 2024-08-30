from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (DataAboutUserIsNotExistException,
                            InvalidTokenFormatException, TokenExpiredException,
                            TokenIsNotExistException, UserIsNotExistException,
                            WrongDataAboutUserException)
from app.users.dao import UserDAO
from app.users.models import Users


def get_token(request: Request):
    token = request.cookies.get("bookmarks_access_token")
    if not token:
        raise TokenIsNotExistException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise InvalidTokenFormatException

    expire: str = payload.get("exp")
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise DataAboutUserIsNotExistException
    elif not user_id.isdigit():
        raise WrongDataAboutUserException

    user: Users = await UserDAO.find_by_id(item_id=int(user_id))
    if not user:
        raise UserIsNotExistException

    return user
