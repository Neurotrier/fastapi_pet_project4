from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .cat import Cat
    from .dog import Dog


class Shelter(Base):
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(200), unique=True)
    cats: Mapped[list["Cat"]] = relationship("Cat", back_populates="shelter")
    dogs: Mapped[list["Dog"]] = relationship("Dog", back_populates="shelter")

    def __str__(self):
        return f"{self.name=}, {self.address=}"

    def __repr__(self):
        return f"{self.name=}, {self.address=}"
