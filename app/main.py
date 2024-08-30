from fastapi import FastAPI

from app.bookmarks.router import router as router_bookmarks
from app.users.router import router as router_auth

app = FastAPI()

app.include_router(router_bookmarks)
app.include_router(router_auth)
