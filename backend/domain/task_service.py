from sqlalchemy.orm import Session

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