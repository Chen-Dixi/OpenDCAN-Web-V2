from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from typing import Optional
from aio_pika.patterns import RPC

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import oauth2_scheme, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, get_db, pwd_context, get_rpc
from repository import crud, dto
router = APIRouter(tags=["Home"])

# utility to verify if a received password matches the hash stored.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# hash a password coming from the user.
def get_password_hash(password):
    return pwd_context.hash(password)

# authenticate and return a user
def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/token")
async def read_token(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# 登录 放在了 main.py 🤔
@router.post("/login", response_model=dto.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    userDto = dto.UserDTO.from_orm(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "username": userDto.username, "token_type": "bearer", "is_admin": userDto.is_admin}

# @router.get("/rpc")
# async def rpc_test(rpc: RPC = Depends(get_rpc)):
#     response = await rpc.proxy.remote_method(task_id=2, model_id = 5)
#     print("Get RPC Response:{}, Type: {}".format(response, type(response)))