from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from src.dogs.schemas import Dog, DogCreate, DogUpdate, DogUpdatePartial
from src.models import db_helper
from .dependencies import dog_by_id

router = APIRouter(tags=["dogs"], prefix="/dogs")


@router.post("/")
async def create_dog(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    dog_in: DogCreate,
) -> Dog:
    return await crud.create_dog(session=session, dog_in=dog_in)


@router.get("/")
async def get_dogs(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)]
):
    return await crud.get_dogs(session=session)


@router.get("/{dog_id}")
async def get_dog(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    dog_id: Annotated[int, Path()],
):
    return await crud.get_dog(session=session, dog_id=dog_id)


@router.put("/{dog_id}")
async def update_dog(
    dog_update: DogUpdate,
    dog: Annotated[Dog, Depends(dog_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    return await crud.update_dog(
        session=session,
        dog=dog,
        dog_update=dog_update,
    )


@router.patch("/{dog_id}")
async def update_dog_partial(
    dog_update: DogUpdatePartial,
    dog: Annotated[Dog, Depends(dog_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    return await crud.update_dog(
        session=session,
        dog=dog,
        dog_update=dog_update,
        partial=True,
    )


@router.delete("/{dog_id}")
async def delete_dog(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    dog_delete: Annotated[Dog, Depends(dog_by_id)],
):
    await crud.delete_dog(session=session, dog_delete=dog_delete)
    return {"status": 200}


@router.get("/shelter/{dog_id}")
async def get_shelter_by_dog(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    dog: Annotated[Dog, Depends(dog_by_id)],
):
    shelter = await crud.get_shelter_by_dog(session=session, dog=dog)
    return {"shelter": shelter}
