from operator import index
from sqlalchemy import BIGINT, Column, ForeignKey, Integer, String, VARCHAR

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(VARCHAR, unique=True, index=True)
    hashed_password = Column(VARCHAR)
    username = Column(VARCHAR)
    display_name = Column(VARCHAR)
    user_type = Column(Integer, default=1)
    is_active = Column(Integer, default=1)
    create_time = Column(BIGINT)
    update_time = Column(BIGINT)

class TargetDatasetRecord(Base):
    __tablename__ = "target_dataset_record"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR)
    description = Column(VARCHAR)
    file_path = Column(VARCHAR)
    create_name = Column(VARCHAR)
    update_name = Column(VARCHAR)
    is_active = Column(Integer, default=1)
    create_time = Column(BIGINT)
    update_time = Column(BIGINT)
