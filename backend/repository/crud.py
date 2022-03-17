from sqlalchemy.orm import Session
from datetime import datetime, timezone
from . import entity, dto

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 返回的都是 entity model
def get_user_by_id(db: Session, user_id: int):
    return db.query(entity.User).filter(entity.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(entity.User).filter(entity.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(entity.User).filter(entity.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(entity.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: dto.CreateUserDTO):
    db_user = entity.User(email = user.email,
                          hashed_password = user.password,
                          username = user.username,
                          user_type = user.user_type,
                          display_name = user.display_name)

    now_time = datetime.now(timezone.utc).microsecond # 毫秒 13位数字
    db_user.create_time = now_time
    db_user.update_time = now_time
    db_user.is_active = 1
    # add that instance object to your database session.
    db.add(db_user)
    # commit the changes to the database (so that they are saved).
    db.commit()
    # refresh your instance (so that it contains any new data from the database, like the generated ID).
    db.refresh(db_user)
    return db_user