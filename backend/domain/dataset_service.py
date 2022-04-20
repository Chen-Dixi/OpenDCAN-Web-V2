from fastapi import HTTPException
import os
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from repository import entity, dto, crud
from common import utils
from settings import DATASET_UPLOAD_PATH, UPLOAD_DATASET_EXTENSIONS

async def upload_target_dataset(file: UploadFile, user: entity.User, db: Session) -> entity.TargetDatasetRecord:
    content = await file.read()
    origin_filename = file.filename
    if not any(origin_filename.endswith(ext) for ext in UPLOAD_DATASET_EXTENSIONS):
        raise HTTPException(status_code=400, detail="File is not an allowed extension.")
    suffix = origin_filename[origin_filename.index('.'):]
    
    filename = utils.generateUUID()+suffix
    save_dir = os.path.join(DATASET_UPLOAD_PATH, 'target_dataset')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    with open(save_path,'wb') as f:
        f.write(content)
    
    create_dto = dto.CreateTargetDatasetRecord(title=origin_filename, file_path=save_path, username = user.username, create_name=user.username)
    db_target_dataset = crud.create_target_dataset_record(db, create_dto)
    return db_target_dataset
    
    
async def unpack_dataset_archive(filepath: str, db: Session):
    extrac_dir = filepath[:filepath.index('.')]
    shutil.unpack_archive(filename=filepath, extract_dir=extrac_dir)
    crud.update_target_dataset(filepath, extrac_dir, db)
    
async def get_target_records(limit: int,
    offset: int,
    username: str,
    ipp: int,
    db: Session):
    
    result = crud.get_target_dataset_records_by_username_count(db, username, offset, limit, return_total_count=True)

    return {"datasets": result[0], "maxPage": (result[1]-1)//ipp + 1 }

async def get_target_selection(username: str, db: Session):
    result = crud.get_target_dataset_records_by_username(db, username)
    return result