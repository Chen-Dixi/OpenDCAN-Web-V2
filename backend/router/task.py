import re
from time import sleep
from typing import List
from os import path

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
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

@router.post("/update/dataset")
async def update_dataset_config(requestDto: dto.UpdateTaskDatasetConfigDto, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # check if task belongs to current user.
    _ = await task_service.get_task_detail(requestDto.task_id, user.username, db)

    await task_service.update_task_dataset(
        requestDto.task_id,
        requestDto.source_id,
        requestDto.source_name,
        requestDto.target_id,
        requestDto.target_name,
        db)

    return {"task_id": requestDto.task_id}

@router.get("/detail/{taskId}", response_model=dto.TaskRecordDto)
async def get_task(taskId: int, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    task_dto = await task_service.get_task_detail(taskId, user.username, db)
    return task_dto

@router.get("/train/{taskId}", response_model=dto.QueryTaskTrainResponse)
async def get_task_train(taskId: int, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # check if task belongs to current user.
    _ = await task_service.get_task_detail(taskId, user.username, db)
    trainings = await task_service.get_task_model_records(task_id=taskId, db=db)
    return {"trainings": trainings, "maxPage": 1}

@router.post("/train/create")
async def create_model_training(createDto: dto.CreateTrainingTaskDto,
                                request: Request,
                                user: entity.User = Depends(get_current_active_user),
                                db: Session = Depends(get_db)
                                ):
    """
    创建异步训练任务
    """# check if task belongs to current user.
    _ = await task_service.get_task_detail(createDto.task_id, user.username, db)
    model_id = await task_service.start_training(createDto, user.username, db, request.app.pika_publisher)

    return {"model": model_id}
    