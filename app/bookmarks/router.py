from fastapi import APIRouter, Depends

from app.bookmarks.dao import BookmarksDAO
from app.bookmarks.schemas import SBookmarks
from app.services import speller
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookmarks", tags=["Закладки"])


@router.post("/create")
async def create_bookmark(
    bookmark: SBookmarks, user: Users = Depends(get_current_user)
):
    title = speller.spelled(bookmark.title)
    body = speller.spelled(bookmark.body)
    await BookmarksDAO.add(title=title, body=body, user_id=user.id)
    return {"changed_text": {"title": title, "body": body}}


@router.get("/view")
async def view_bookmarks(user: Users = Depends(get_current_user)):
    bookmarks = await BookmarksDAO.get_all_bookmarks(user_id=user.id)
    return bookmarks
