from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.models import Shelter, Cat
from src.shelters.schemas import (
    ShelterCreate,
    ShelterUpdate,
    ShelterUpdatePartial,
)


async def create_shelter(session: AsyncSession, shelter_in: ShelterCreate) -> Shelter:
    shelter = Shelter(**shelter_in.model_dump())
    session.add(shelter)
    await session.commit()
    return shelter


async def get_shelters(session: AsyncSession) -> list[Shelter]:
    stmt = select(Shelter).order_by(Shelter.id)
    result = await session.execute(stmt)
    shelters = result.scalars().all()
    return list(shelters)


async def get_shelter(session: AsyncSession, shelter_id: int) -> Shelter | None:
    return await session.get(Shelter, shelter_id)


async def update_shelter(
    session: AsyncSession,
    shelter: Shelter,
    shelter_update: ShelterUpdate | ShelterUpdatePartial,
    partial: bool = False,
) -> Shelter:
    for name, value in shelter_update.model_dump(exclude_unset=partial).items():
        setattr(shelter, name, value)
    await session.commit()
    return shelter


async def delete_shelter(session: AsyncSession, shelter_delete: Shelter) -> None:
    await session.delete(shelter_delete)
    await session.commit()


async def get_cats_by_shelter(session: AsyncSession, shelter: Shelter) -> Any:
    stmt = (
        select(Shelter)
        .options(selectinload(Shelter.cats))
        .where(Shelter.id == shelter.id)
    )
    shelter = await session.scalar(stmt)
    result = {"cats": {}}

    for cat in shelter.cats:
        result.get("cats")[cat.name] = cat

    return result
