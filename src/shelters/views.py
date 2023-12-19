from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from src.models import db_helper
from src.shelters.schemas import (
    ShelterCreate,
    ShelterUpdate,
    ShelterUpdatePartial,
    Shelter,
)
from .dependencies import shelter_by_id

router = APIRouter(tags=["shelters"], prefix="/shelters")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login/",
)


@router.post("/")
async def create_shelter(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    shelter_in: ShelterCreate,
):
    return await crud.create_shelter(session=session, shelter_in=shelter_in)


@router.get("/")
async def get_shelters(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    token: str = Depends(oauth2_scheme),
):
    print(token)
    return await crud.get_shelters(session=session)


@router.get("/{shelter_id}")
async def get_shelter(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    shelter_id: Annotated[int, Path()],
):
    return await crud.get_shelter(session=session, shelter_id=shelter_id)


@router.put("/{shelter_id}")
async def update_shelter(
    shelter_update: ShelterUpdate,
    shelter: Annotated[Shelter, Depends(shelter_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    return await crud.update_shelter(
        session=session,
        shelter=shelter,
        shelter_update=shelter_update,
    )


@router.patch("/{shelter_id}")
async def update_shelter_partial(
    shelter_update: ShelterUpdatePartial,
    shelter: Shelter = Depends(shelter_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_shelter(
        session=session,
        shelter=shelter,
        shelter_update=shelter_update,
        partial=True,
    )


@router.delete("/{shelter_id}")
async def delete_shelter(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    shelter_delete: Annotated[Shelter, Depends(shelter_by_id)],
):
    await crud.delete_shelter(session=session, shelter_delete=shelter_delete)
    return {"status": 200}


@router.get("/cats/{shelter_id}")
async def get_cats_by_shelter(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    shelter: Annotated[Shelter, Depends(shelter_by_id)],
):
    return await crud.get_cats_by_shelter(session=session, shelter=shelter)
