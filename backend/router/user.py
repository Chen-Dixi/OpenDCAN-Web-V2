from sys import prefix
from fastapi import APIRouter, Depends
from domain.model import User

from dependencies import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]