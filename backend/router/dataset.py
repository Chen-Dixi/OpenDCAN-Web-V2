from typing import List
from os import path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db, pwd_context
from repository import entity, dto

from domain import dataset_service

router = APIRouter(
    prefix="/dataset",
    tags=["dataset"]
)

async def unzip_the_target_dataset(file_path: str, db: Session):
    await dataset_service.unpack_dataset_archive(file_path, db)

async def unzip_the_source_dataset(dataset_id: int, file_path: str, db: Session):
    await dataset_service.unpack_source_dataset_archive(dataset_id, file_path, db)

@router.post("/target/upload")
async def uplaod_target_dataset(file: UploadFile, background_tasks: BackgroundTasks, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    🤔 这里是不是创建了两个 db session. answer: 不会, 拿到的是同一个, 会从类似 threadLocal的东西里去取db session
    <sqlalchemy.orm.session.Session object at 0x7f9b927e4dd8>\n
    <sqlalchemy.orm.session.Session object at 0x7f9b927e4dd8>\n
    上传压缩后的数据集
    1. 解压
    2. 重命名 带uuid
    3. 更新数据库 表 target_dataset_record
    4. 返回
    """
    db_dataset_record = dataset_service.upload_target_dataset(file, user, db)

    # send asynchronous message to unzip the file
    background_tasks.add_task(unzip_the_target_dataset, (await db_dataset_record).file_path, db)
    
    return {"filename": file.filename}

@router.post("/source/upload")
async def uplaod_source_dataset(file: UploadFile, background_tasks: BackgroundTasks, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    上传压缩后的数据集
    1. 解压
    2. 重命名 带uuid
    3. 统计class 信息
    4. 更新数据库 表 source_dataset_record
    5. 返回
    """
    # 权限校验
    if (user.user_type != 1):
        raise HTTPException(
            status_code=401,
            detail="Only Administrator can upload source dataset",
            headers={"WWW-Authenticate": "Bearer"})
    
    source_dto = await dataset_service.upload_source_dataset(file, user, db)
    # 解压任务放在 后台任务中去执行
    background_tasks.add_task(unzip_the_source_dataset, source_dto.id, source_dto.file_path, db)

    return {"filename": source_dto.title}


@router.delete("/target/delete/{dataset_name}")
async def delete_file(dataset_name:str):
    
    return {'detail':0}

@router.get("/target/list", response_model = dto.QueryTargetDatasetResponse)
async def get_target_dataset_list(limit: int,
    offset: int,
    ipp: int, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):

    result = await dataset_service.get_target_records(limit, offset, user.username, ipp, db)
    # records_dto = [dto.TargetDatasetDto.from_orm(record) for record in records]
    return result

@router.get("/target/list_selection", response_model=dto.QueryTargetDatasetSelectionResponse)
async def get_target_dataset_selection(user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    result = await dataset_service.get_target_selection(user.username, db)
    return {'selections': result}

@router.get("/target/get", response_model=dto.TargetDatasetRecordDto)
async def get_source_dataset(dataset_id:int, user:entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_target = await dataset_service.get_target_single_record(dataset_id, user.username, db)
    return db_target

@router.get("/source/list", response_model = dto.QuerySourceDatasetResponse)
async def get_source_dataset_list(limit: int,
    offset: int,
    ipp: int, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    
    # if (user.user_type != 1): 
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Only Administrator can upload source dataset",
    #         headers={"WWW-Authenticate": "Bearer"})

    result = await dataset_service.get_source_records(limit, offset, ipp, db)
    # records_dto = [dto.TargetDatasetDto.from_orm(record) for record in records]
    return result

@router.get("/source/list_selection", response_model=dto.QuerySourceDatasetSelectionResponse)
async def get_source_dataset_selection(user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    result = await dataset_service.get_source_selection(user.username, db)
    return {'selections': result}

@router.get("/source/get", response_model=dto.SourceDatasetRecordDto)
async def get_source_dataset(dataset_id:int, user:entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_source = await dataset_service.get_source_single_record(dataset_id, db)
    return db_source

@router.post("/target/update")
async def update_source_dataste(updateDto: dto.UpdateDatasetRecord, user:entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    await dataset_service.update_target_basic_information(updateDto.id,
                                                    updateDto.title,
                                                    updateDto.description,
                                                    user.username,
                                                    db)
    return {"dataset_id": updateDto.id}

@router.post("/source/update")
async def update_source_dataste(updateDto: dto.UpdateDatasetRecord, user:entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    await dataset_service.update_source_basic_information(updateDto.id,
                                                    updateDto.title,
                                                    updateDto.description,
                                                    user,
                                                    db)
    return {"dataset_id": updateDto.id}