from fastapi import APIRouter, Depends

from typing import Annotated

from app.auth.actions import get_current_user


router = APIRouter(prefix="/api", tags=["api"])


@router.get("/me")
async def get_me_info(current_user: Annotated[tuple, Depends(get_current_user)]):
    return current_user