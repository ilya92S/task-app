from datetime import date, time
from typing import Any

from pydantic import BaseModel, Field, model_validator

class TaskSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    date: date
    time: str
    comment: str | None = None
    category_id: int

    class Config:
        from_attributes = True



    # @model_validator(mode="before")
    # @classmethod
    # def check_name_or_comment(cls, data):
    #     if data["name"] is None:
    #         data["name"] = "jjjjjjjjjjjjj"
    #     for d in data:
    #         print(d)
    #
    #     return data
