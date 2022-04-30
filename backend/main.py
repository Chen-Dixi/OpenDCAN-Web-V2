from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import user, dataset, task, base_router
from settings import allow_cors_origins
from mq.rabbitmq import PikaPublisher
# create database table, skip this if there already has one
# entity.Base.metadata.create_all(bind=engine)

class DixiFastAPI(FastAPI):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_publisher = PikaPublisher()


# app = FastAPI(docs_url='/api/v1/docs')
app = DixiFastAPI(docs_url='/api/v1/docs')
app.include_router(base_router.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(dataset.router, prefix="/api/v1")
app.include_router(task.router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# # utility to verify if a received password matches the hash stored.
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # hash a password coming from the user.
# def get_password_hash(password):
#     return pwd_context.hash(password)

# # authenticate and return a user
# def authenticate_user(username: str, password: str, db: Session):
#     user = crud.get_user_by_username(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# @app.get("/token")
# async def read_token(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

# # 登录 放在了 main.py 🤔
# @app.post("/login", response_model=dto.Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     userDto = dto.UserDTO.from_orm(user)
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "username": userDto.username, "token_type": "bearer", "is_admin": userDto.is_admin}
