from typing import Annotated

from fastapi import Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from src.models import db_helper
from src.cats import crud


async def cat_by_id(
    cat_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    cat = await crud.get_cat(session=session, cat_id=cat_id)
    if cat is not None:
        return cat

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cat {cat_id} not found!",
    )
