from typing import List
from matplotlib import offsetbox
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from passlib.context import CryptContext

from . import entity, dto
from settings import RECORD_LIMIT, TASK_LIST_IPP

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

    # now_time = datetime.now(timezone.utc).microsecond # 毫秒 13位数字
    now_time = datetime.now(timezone.utc)
    now_time = int(datetime.timestamp(now_time)*1000)
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


# ==================
# Target Dataset Record
def create_target_dataset_record(db: Session, create_dto: dto.CreateTargetDatasetRecord):
    db_target_dataset = entity.TargetDatasetRecord(file_path = create_dto.file_path,
                                                   username = create_dto.username,
                                                   create_name = create_dto.create_name,
                                                   update_name = create_dto.create_name)
    now_time = datetime.now(timezone.utc)
    now_time = int(datetime.timestamp(now_time)*1000)
    db_target_dataset.create_time = now_time
    db_target_dataset.update_time = now_time
    db_target_dataset.is_active = 1
    db_target_dataset.state = 2
    db.add(db_target_dataset)
    db.commit()
    db.refresh(db_target_dataset)
    return db_target_dataset

def update_target_dataset(file_path, folder_path, db: Session):
    record = db.query(entity.TargetDatasetRecord).filter(entity.TargetDatasetRecord.file_path == file_path).update({'state':1,'file_path':folder_path})
    db.commit()

def get_target_dataset_records_by_username(db: Session, username: str, offset:int = 0, limit = RECORD_LIMIT, return_total_count: bool = False) -> List[entity.TargetDatasetRecord]:
    records = db.query(entity.TargetDatasetRecord) \
             .filter(entity.TargetDatasetRecord.username == username, entity.TargetDatasetRecord.is_active == 1) \
             .offset(offset) \
             .limit(limit) \
             .all()
    if return_total_count:
        count = db.query(entity.TargetDatasetRecord) \
             .filter(entity.TargetDatasetRecord.username == username, entity.TargetDatasetRecord.is_active == 1).count()
        return records, count
    return records

def get_target_dataset_records_by_username_count(db: Session, username: str) -> int:
    return db.query(entity.TargetDatasetRecord) \
             .filter(entity.TargetDatasetRecord.username == username, entity.TargetDatasetRecord.is_active == 1).count()

def get_task_records_by_username(
    db: Session,
    username: str,
    offset: int,
    limit: int = TASK_LIST_IPP
    ):
    records = db.query(entity.TaskRecord) \
                .filter(entity.TaskRecord.username == username, entity.TaskRecord.is_active == 1) \
                .order_by(entity.TaskRecord.update_time) \
                .offset(offset) \
                .limit(limit) \
                .all()
    count = db.query(entity.TaskRecord) \
                .filter(entity.TaskRecord.username == username, entity.TaskRecord.is_active == 1) \
                .count()

    return records, count

def create_task_record(db: Session, task_name: str, username: str):
    """
    新建任务 task_record
    """
    db_task = entity.TaskRecord(
        name = task_name,
        username = username
    )
    
    now_time = datetime.now(timezone.utc)
    now_time = int(datetime.timestamp(now_time)*1000)
    db_task.create_time = now_time
    db_task.update_time = now_time
    db_task.is_active = 1
    db_task.state = 2
    db_task.create_name = username
    db_task.update_name = username

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task