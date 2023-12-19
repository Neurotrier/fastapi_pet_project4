from sqlalchemy.orm import Mapped, relationship, declared_attr

from .animal import Animal


class Dog(Animal):
    @declared_attr
    def shelter(cls) -> Mapped["Shelter"]:
        return relationship("Shelter", back_populates="dogs")

    def __str__(self):
        return f"{self.name=}"

    def __repr__(self):
        return f"{self.name=}"
