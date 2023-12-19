from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from src.cats.schemas import Cat, CatCreate, CatUpdate, CatUpdatePartial
from src.models import db_helper
from .dependencies import cat_by_id

router = APIRouter(tags=["cats"], prefix="/cats")


@router.post("/")
async def create_cat(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    cat_in: CatCreate,
) -> Cat:
    return await crud.create_cat(session=session, cat_in=cat_in)


@router.get("/")
async def get_cats(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)]
):
    cats = await crud.get_cats(session=session)
    res = {}
    for cat in cats:
        res[cat.name] = cat
    return {"cats": res}


@router.get("/params")
async def get_cats_params(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    cat_name: Annotated[str, Query()],
    cat_color: Annotated[str, Query()],
    cat_shelter_id: Annotated[int, Query()],
    strict: Annotated[bool, Query()],
):
    cats = await crud.get_cats_params(
        session=session,
        cat_name=cat_name,
        cat_color=cat_color,
        shelter_id=cat_shelter_id,
        strict=strict,
    )
    res = {}
    for cat in cats:
        res[cat.name] = cat
    return {"cats": res}


@router.get("/{cat_id}")
async def get_cat(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    cat_id: Annotated[int, Path()],
):
    return await crud.get_cat(session=session, cat_id=cat_id)


@router.put("/{cat_id}")
async def update_cat(
    cat_update: CatUpdate,
    cat: Annotated[Cat, Depends(cat_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    return await crud.update_cat(
        session=session,
        cat=cat,
        cat_update=cat_update,
    )


@router.patch("/{cat_id}")
async def update_cat_partial(
    cat_update: CatUpdatePartial,
    cat: Annotated[Cat, Depends(cat_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    return await crud.update_cat(
        session=session,
        cat=cat,
        cat_update=cat_update,
        partial=True,
    )


@router.delete("/{cat_id}")
async def delete_cat(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    cat_delete: Annotated[Cat, Depends(cat_by_id)],
):
    await crud.delete_cat(session=session, cat_delete=cat_delete)
    return {"status": 200}


@router.get("/shelter/{cat_id}")
async def get_shelter_by_cat(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    cat: Annotated[Cat, Depends(cat_by_id)],
):
    shelter = await crud.get_shelter_by_cat(session=session, cat=cat)
    return {"shelter": shelter}
