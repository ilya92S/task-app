from typing import Annotated
from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


id_pk = Annotated[int, mapped_column(primary_key=True)]


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[id_pk]
    name: Mapped[str]
    date: Mapped[date]
    time: Mapped[str]
    comment: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("userprofile.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[id_pk]
    type: Mapped[str | None]
    name: Mapped[str]