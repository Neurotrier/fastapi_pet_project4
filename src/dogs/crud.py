from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from sqlalchemy.orm import joinedload

from src.dogs.schemas import DogCreate, DogUpdate, DogUpdatePartial
from src.models import Dog, Shelter


async def create_dog(session: AsyncSession, dog_in: DogCreate) -> Dog:
    dog = Dog(**dog_in.model_dump())
    result = await session.execute(select(Shelter).where(Shelter.id == dog.shelter_id))
    shelter = result.scalar_one_or_none()
    if shelter:
        session.add(dog)
        await session.commit()
        return dog
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shelter {dog.shelter_id} not found!",
        )


async def get_dogs(session: AsyncSession) -> list[Dog]:
    stmt = select(Dog).order_by(Dog.id)
    result = await session.execute(stmt)
    dogs = result.scalars().all()
    return list(dogs)


async def get_dog(session: AsyncSession, dog_id: int) -> Dog | None:
    return await session.get(Dog, dog_id)


async def update_dog(
    session: AsyncSession,
    dog: Dog,
    dog_update: DogUpdate | DogUpdatePartial,
    partial: bool = False,
) -> Dog:
    for name, value in dog_update.model_dump(exclude_unset=partial).items():
        setattr(dog, name, value)
    await session.commit()
    return dog


async def delete_dog(session: AsyncSession, dog_delete: Dog) -> None:
    await session.delete(dog_delete)
    await session.commit()


async def get_shelter_by_dog(session: AsyncSession, dog: Dog) -> Shelter:
    stmt = select(Dog).options(joinedload(Dog.shelter)).where(Dog.id == dog.id)
    dog = await session.scalar(stmt)
    return dog.shelter
