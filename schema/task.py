from datetime import date, time
from typing import Any

from pydantic import BaseModel, Field, model_validator


class TaskSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    date: date
    time: str
    comment: str | None = None
    user_id: int
    category_id: int

    class Config:
        from_attributes = True


class TaskCreateSchema(BaseModel):
    name: str | None = None
    date: date
    time: str
    comment: str | None = None
    category_id: int
