from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from sqlalchemy.orm import joinedload

from src.cats.schemas import CatCreate, CatUpdate, CatUpdatePartial
from src.models import Cat, Shelter


async def create_cat(session: AsyncSession, cat_in: CatCreate) -> Cat:
    cat = Cat(**cat_in.model_dump())
    result = await session.execute(select(Shelter).where(Shelter.id == cat.shelter_id))
    shelter = result.scalar_one_or_none()
    if shelter:
        session.add(cat)
        await session.commit()
        return cat
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shelter {cat.shelter_id} not found!",
        )


async def get_cats(session: AsyncSession) -> list[Cat]:
    stmt = select(Cat).order_by(Cat.id)
    result = await session.execute(stmt)
    cats = result.scalars().all()
    return list(cats)


async def get_cat(session: AsyncSession, cat_id: int) -> Cat | None:
    return await session.get(Cat, cat_id)


async def update_cat(
    session: AsyncSession,
    cat: Cat,
    cat_update: CatUpdate | CatUpdatePartial,
    partial: bool = False,
) -> Cat:
    for name, value in cat_update.model_dump(exclude_unset=partial).items():
        setattr(cat, name, value)
    await session.commit()
    return cat


async def delete_cat(session: AsyncSession, cat_delete: Cat) -> None:
    await session.delete(cat_delete)
    await session.commit()


async def get_shelter_by_cat(session: AsyncSession, cat: Cat) -> Shelter:
    stmt = select(Cat).options(joinedload(Cat.shelter)).where(Cat.id == cat.id)
    cat = await session.scalar(stmt)
    return cat.shelter


async def get_cats_params(
    session: AsyncSession,
    cat_name: str,
    cat_color: str,
    shelter_id: int,
    strict: bool = True,
) -> list[Cat]:
    stmt = (
        (
            select(Cat).filter(
                or_(
                    Cat.name.ilike(f"%{cat_name}%"),
                    Cat.color == cat_color,
                    Cat.shelter_id == shelter_id,
                )
            )
        )
        if not strict
        else (
            select(Cat)
            .filter(Cat.name.ilike(f"%{cat_name}%"))
            .filter(Cat.color == cat_color)
            .filter(Cat.shelter_id == shelter_id)
        )
    )
    result = await session.execute(stmt)
    cats = result.scalars().all()
    return list(cats)
