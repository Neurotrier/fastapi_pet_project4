from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from src.models import db_helper
from src.dogs import crud


async def dog_by_id(
    dog_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dog = await crud.get_dog(session=session, dog_id=dog_id)
    if dog is not None:
        return dog

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cat {dog_id} not found!",
    )
