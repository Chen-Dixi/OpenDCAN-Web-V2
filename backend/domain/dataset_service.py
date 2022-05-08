import os
import shutil
import json
from datetime import datetime, timezone

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from repository import entity, dto, crud
from common import utils
from settings import DATASET_UPLOAD_PATH, UPLOAD_DATASET_EXTENSIONS, DIRIGNORE

async def upload_target_dataset(file: UploadFile, user: entity.User, db: Session) -> entity.TargetDatasetRecord:
    """
    目标域数据集上传服务
    """
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


async def upload_source_dataset(file: UploadFile, user: entity.User, db: Session) -> dto.SourceDatasetRecordDto:
    """
    源域数据集上传服务
    """
    content = await file.read()
    origin_filename = file.filename
    if not any(origin_filename.endswith(ext) for ext in UPLOAD_DATASET_EXTENSIONS):
        raise HTTPException(status_code=400, detail="File is not an allowed extension.")
    suffix = origin_filename[origin_filename.index('.'):]
    
    filename = utils.generateUUID()+'_'+origin_filename
    save_dir = os.path.join(DATASET_UPLOAD_PATH, 'source_dataset')
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    with open(save_path,'wb') as f:
        f.write(content)
    
    create_dto = dto.CreateSourceDatasetRecordDto(title=origin_filename, file_path=save_path, create_name=user.username)
    db_source_dataset = crud.create_source_dataset_record(db, create_dto)
    
    return dto.SourceDatasetRecordDto.from_orm(db_source_dataset)
    
async def unpack_dataset_archive(dataset_id: int, filepath: str, db: Session):
    extrac_dir = filepath[:filepath.index('.')]
    
    shutil.unpack_archive(filename=filepath, extract_dir=extrac_dir)
    crud.update_target_dataset(dataset_id, {'state':1,'file_path':extrac_dir}, db)

def find_classes(dir):
    classes = [d.name for d in os.scandir(dir) if d.is_dir() and d.name != DIRIGNORE]
    classes.sort() # 一定要排序，这样才能和 训练时一致
    return classes

async def unpack_source_dataset_archive(dataset_id: int, filepath: str, db: Session):
    """
    解压后还要统计 class 标签, 所有的classes 写入数据库
    """
    extrac_dir = filepath[:filepath.index('.')]
    # 这里还要处理文件夹数据
    shutil.unpack_archive(filename=filepath, extract_dir=extrac_dir)
    classes = find_classes(extrac_dir)

    crud.update_source_dataset(dataset_id, {'file_path': extrac_dir, "labels": json.dumps(classes), "label_num": len(classes), "state":1}, db)
    
async def get_target_records(limit: int,
    offset: int,
    username: str,
    ipp: int,
    db: Session):
    
    result = crud.get_target_dataset_records_by_username_count(db, username, offset, limit, return_total_count=True)

    return {"datasets": result[0], "maxPage": (result[1]-1)//ipp + 1 }

async def get_target_selection(username: str, db: Session):
    result = crud.get_target_dataset_ready_records_by_username(db, username)
    return result

async def get_target_single_record(dataset_id: int, username: str, db: Session):
    db_target = crud.get_target_dataset_record_by_id(db = db, recordId = dataset_id)
    if db_target is None:
        raise HTTPException(status_code=400, detail="Data not found")
    if db_target.username != username:
        raise HTTPException(status_code=401, detail="Unauthorized access to data")
    return db_target

async def get_source_records(limit: int,
    offset: int,
    ipp: int,
    db: Session):
    
    result = crud.get_source_dataset_records_count(db, offset, limit)

    return {"datasets": result[0], "maxPage": (result[1]-1)//ipp + 1 }

async def get_source_selection(username: str, db: Session):
    result = crud.get_source_dataset_ready_records(db)
    return result

async def get_source_single_record(dataset_id: int, db: Session):
    db_source = crud.get_source_dataset_record_by_id(db = db, recordId = dataset_id)
    if db_source is None:
        raise HTTPException(status_code=400, detail="Data not found")
    return db_source

async def update_target_basic_information(dataset_id: int, title: str, description: str, username: str, db: Session):
    db_dataset = crud.get_target_dataset_record_by_id(db, dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=400, detail="Data not found")

    if db_dataset.username != username:
        raise HTTPException(status_code=401, detail="Unauthorized access to data")

    now_time = datetime.now(timezone.utc)
    now_time = int(datetime.timestamp(now_time)*1000)
    toUpdate = {
        'title': title,
        'description': description,
        'update_time': now_time
    }
    crud.update_target_dataset(dataset_id, toUpdate, db)

async def update_source_basic_information(dataset_id: int, title: str, description: str, user: entity.User, db: Session):
    db_dataset = crud.get_source_dataset_record_by_id(db, dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=400, detail="Data not found")

    if user.user_type != 1:
        raise HTTPException(status_code=401, detail="Unauthorized access to data")
        
    now_time = datetime.now(timezone.utc)
    now_time = int(datetime.timestamp(now_time)*1000)
    print(title)
    print(description)
    
    toUpdate = {
        'title': title,
        'description': description,
        'update_time': now_time
    }
    crud.update_source_dataset(dataset_id, toUpdate, db)