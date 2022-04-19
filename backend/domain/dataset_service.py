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
    filename = file.filename
    if not any(filename.endswith(ext) for ext in UPLOAD_DATASET_EXTENSIONS):
        raise HTTPException(status_code=400, detail="File is not an allowed extension.")
    suffix = filename[filename.index('.'):]
    
    filename = utils.generateUUID()+suffix
    save_dir = os.path.join(DATASET_UPLOAD_PATH, 'target_dataset')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    with open(save_path,'wb') as f:
        f.write(content)
    
    create_dto = dto.CreateTargetDatasetRecord(file_path=save_path, username = user.username, create_name=user.username)
    db_target_dataset = crud.create_target_dataset_record(db, create_dto)
    return db_target_dataset
    
    
async def unpack_dataset_archive(filepath: str, db: Session):
    extrac_dir = filepath[:filepath.index('.')]
    shutil.unpack_archive(filename=filepath, extract_dir=extrac_dir)
    crud.update_target_dataset(filepath, extrac_dir, db)
    
async def get_target_records(createDto: dto.QueryTargetDatasetDto, db: Session):
    
    return crud.get_target_dataset_records_by_username(db, createDto.username, createDto.offset, createDto.limit)
    