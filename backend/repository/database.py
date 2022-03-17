from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:0907_cdx@localhost:3306/opendcan_v2?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    pool_timeout=30
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()