from sqlalchemy.orm import Session
from datetime import datetime, timezone

from fastapi import HTTPException, status

from repository import entity, dto, crud

async def get_task_records(ipp: int,
    offset: int,
    username: str, db: Session):

    result = crud.get_task_records_by_username(db, username, offset, ipp)
    
    return {"tasks": result[0], "maxPage": (result[1]-1)//ipp + 1 }

async def create_task_record(task_name: str, username: str, db: Session) -> dto.TaskRecordDto:
    task = crud.create_task_record(db, task_name, username)
    return dto.TaskRecordDto.from_orm(task)

async def get_task_detail(taskId: int, username: str, db: Session) -> dto.TaskRecordDto:
    db_task = crud.get_task_record_by_id(db, taskId=taskId)
    if db_task is None:
        raise HTTPException(status_code=400, detail="Data not found")
    if db_task.username != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access to data")
    
    return dto.TaskRecordDto.from_orm(db_task)

async def update_task_dataset(task_id: int,
    source_id: int,
    source_name: str,
    target_id: int,
    target_name: str,
    db: Session):

    now_time = datetime.now(timezone.utc)
    now_time = int(datetime.timestamp(now_time)*1000)

    crud.update_task_record_by_id(
        task_id=task_id, 
        toUpdate={"source_id": source_id, "source_name": source_name, "target_id": target_id, "target_name": target_name, "update_time": now_time},
        db=db)

async def get_task_model_records(
    task_id: int,
    db: Session):
    return crud.get_model_records_by_taskId(task_id, db)

async def start_training(createDto: dto.CreateTrainingTaskDto, username: str, db: Session)->int:
    db_model_record = crud.create_model_record(db, createDto.task_id, 
                             username, 
                             createDto.source_id, createDto.source_name,
                             createDto.target_id, createDto.target_name)
    # TBD发送消息，提交一个 训练任务
    
    # 更新任务状态，state=2 TRAINING
    now_time = datetime.now(timezone.utc)
    now_time = int(datetime.timestamp(now_time)*1000)
    crud.update_task_record_by_id(createDto.task_id, {"state": 2, "update_time":now_time, "update_name":username}, db)
    return db_model_record.id