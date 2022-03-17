from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from domain.model import *
from router import user
from dependencies import oauth2_scheme, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, get_db

from repository import dto, crud

# create database table, skip this if there already has one
# entity.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)

# utility to verify if a received password matches the hash stored.
def verify_password(plain_password, hashed_password):
    return crud.pwd_context.verify(plain_password, hashed_password)

# hash a password coming from the user.
def get_password_hash(password):
    return crud.pwd_context.hash(password)

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

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.post("/token", response_model=dto.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}