from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

from .base import Base

if TYPE_CHECKING:
    from .shelter import Shelter


class Animal(Base):
    __abstract__ = True
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]
    color: Mapped[str]

    @declared_attr
    def shelter_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey("shelter.id"))
