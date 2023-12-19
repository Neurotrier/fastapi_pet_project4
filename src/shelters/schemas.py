from pydantic import BaseModel, ConfigDict


class ShelterBase(BaseModel):
    name: str
    address: str


class ShelterCreate(ShelterBase):
    pass


class ShelterUpdate(ShelterBase):
    pass


class ShelterUpdatePartial(ShelterBase):
    name: str | None = None
    address: str | None = None


class Shelter(ShelterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
