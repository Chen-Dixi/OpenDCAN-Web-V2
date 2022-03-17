from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from repository.database import SessionLocal
from repository import crud, entity, dto

SECRET_KEY = "e5ac7747a0ab5636e9705164c49f4e4ea9c5ee33321d3401b62253e8dd1a628e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # jwt.decode will verify a JWT string's signature and validates reserved claims
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expire = payload.get("exp")
        
        # if int(datetime.utcnow()) > expire:
        #     raise credentials_exception
        # verify it
        if username is None:
            raise credentials_exception
        token_data = dto.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: entity.User = Depends(get_current_user)):
    if current_user.is_active != 1: # replace magic number
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user