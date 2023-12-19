from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from src.models import db_helper
from src.shelters import crud


async def shelter_by_id(
    shelter_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    shelter = await crud.get_shelter(session=session, shelter_id=shelter_id)
    if shelter is not None:
        return shelter

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Shelter {shelter_id} not found!",
    )
