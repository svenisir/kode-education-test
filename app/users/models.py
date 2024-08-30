from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.bookmarks.models import Bookmarks
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str]

    bookmarks: Mapped[list["Bookmarks"]] = relationship(
        "Bookmarks", back_populates="user"
    )

    def __str__(self):
        return f"User: {self.email}"
