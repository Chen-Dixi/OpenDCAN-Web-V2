from typing import List
from os import path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db, pwd_context
from repository import entity, dto

from domain import task_service

router = APIRouter(
    prefix="/task",
    tags=["Task"]
)

@router.get("/list", response_model=dto.QueryTaskRecordResponse)
async def get_target_dataset_list(ipp: int,
    offset: int,
    user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):

    result = await task_service.get_task_records(ipp, offset, user.username, db)
    return result

@router.post("/create", response_model = dto.TaskRecordDto)
async def create_task(createDto: dto.CreateTaskDto, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    task_dto = await task_service.create_task_record(createDto.task_name, user.username, db)
    return task_dto