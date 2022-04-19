from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db, pwd_context
from repository.database import SessionLocal
from repository import dto, entity, crud

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@router.get("/me", response_model=dto.UserDTO)
async def read_users_me(current_user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return current_user

@router.get("/me/items/")
async def read_own_items(current_user: entity.User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.display_name}]

@router.post("/register", response_model=dto.UserDTO)
def create_user(user: dto.CreateUserDTO, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # automatically orm
    user.password = pwd_context.hash(user.password)
    return crud.create_user(db, user)