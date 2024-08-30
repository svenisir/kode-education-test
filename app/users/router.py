from fastapi import APIRouter, Response

from app.exceptions import (UserAlreadyExistException,
                            UserIsNotAuthenticatedException)
from app.users.auth import (authenticate_user, create_access_token,
                            get_hashed_password)
from app.users.dao import UserDAO
from app.users.schemas import SUser

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register")
async def register_user(user_data: SUser):
    existing_user = await UserDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_hashed_password(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUser):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise UserIsNotAuthenticatedException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("bookmarks_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("bookmarks_access_token")
