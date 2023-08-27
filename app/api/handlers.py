from fastapi import APIRouter, Depends

from typing import Annotated

from app.auth.actions import get_current_user_from_token_payload


router = APIRouter(prefix="/api", tags=["api"])


@router.get("/me")
async def get_me_info(currentc_user: Annotated[tuple, Depends(get_current_user_from_token_payload)]):
    print(currentc_user)