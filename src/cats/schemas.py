from pydantic import BaseModel, ConfigDict


class CatBase(BaseModel):
    name: str
    age: int
    color: str
    tail_length: int
    shelter_id: int


class CatCreate(CatBase):
    pass


class CatUpdate(CatBase):
    pass


class CatUpdatePartial(CatBase):
    name: str | None = None
    age: int | None = None
    color: str | None = None
    tail_length: int | None = None


class Cat(CatBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
