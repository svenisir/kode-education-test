from pydantic import BaseModel, Field


class SBookmarks(BaseModel):
    title: str = Field(description="Укажите название заметки")
    body: str = Field(description="Текст вашей заметки")

    class Config:
        json_schema_extra = {"example": {"title": "Без названия", "body": "..."}}
