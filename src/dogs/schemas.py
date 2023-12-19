from pydantic import BaseModel, ConfigDict


class DogBase(BaseModel):
    name: str
    age: int
    color: str
    shelter_id: int


class DogCreate(DogBase):
    pass


class DogUpdate(DogBase):
    pass


class DogUpdatePartial(DogBase):
    name: str | None = None
    age: int | None = None
    color: str | None = None


class Dog(DogBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
