from sqlalchemy.orm import Mapped, declared_attr, relationship

from .animal import Animal


class Cat(Animal):
    tail_length: Mapped[int]

    @declared_attr
    def shelter(cls) -> Mapped["Shelter"]:
        return relationship("Shelter", back_populates="cats")

    def __str__(self):
        return f"{self.name=}"

    def __repr__(self):
        return f"{self.name=}"
