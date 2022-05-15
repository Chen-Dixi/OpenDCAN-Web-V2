import os
import json
from fastapi import APIRouter, Depends, Request, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db, get_rabbitmq_blockingconnection
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
    """查询发起过的训练记录，显示在 任务详情'Train'栏目页的列表中
    """
    # check if task belongs to current user.
    _ = await task_service.get_task_detail(taskId, user.username, db)
    trainings = await task_service.get_task_model_records(task_id=taskId, db=db)
    return {"trainings": trainings, "maxPage": 1}

@router.post("/train/create")
async def create_model_training(createDto: dto.CreateTrainingTaskDto,
                                pika_publisher = Depends(get_rabbitmq_blockingconnection),
                                user: entity.User = Depends(get_current_active_user),
                                db: Session = Depends(get_db)
                                ):
    """
    创建异步训练任务
    """# check if task belongs to current user.
    _ = await task_service.get_task_detail(createDto.task_id, user.username, db)
    model_id = await task_service.start_training(createDto, user.username, db, pika_publisher)

    return {"model": model_id}
    
@router.get("/play/model/list/{task_id}", response_model=dto.QueryModelSelectionResponse)
async def get_model_selection_for_play(task_id: int, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """返回训练完成的模型对象, modelrecord.state == 1
    """

    selections = await task_service.get_ready_model_selections(task_id, user.username, db)
    return {"selections": selections}
    
@router.post("/play/inference/sample", response_model=dto.StartInferenceSampleResponse)
async def inference_sample(file: UploadFile,
                           task_id: int = Form(...), model_id: int = Form(...),
                           pika_publisher = Depends(get_rabbitmq_blockingconnection),
                           user: entity.User = Depends(get_current_active_user),
                           db: Session = Depends(get_db)):
    
    # check if task belongs to current user.
    _ = await task_service.get_task_detail(task_id, user.username, db)

    # 文件要发送过去？ 临时存储文件, 消息传递一个文件名字过去，训练完后删除
    check_id = await task_service.start_inference_single_sample(file, model_id, pika_publisher, db)
    return {"check_id": check_id}

@router.get("/play/sample/{check_id}/check", response_model=dto.CheckInferenceSampleResponse)
async def inference_sample_check(check_id: str, request: Request):
    """异步接口，提交一个样本进行预测后，通过此接口查询模型推理结果
    """
    cache_key = "inferencesample:{}".format(check_id)
    redis = request.app.state.redis
    value = await redis.get(cache_key)

    if value is None:
        return {"state":"PENDING"}
    
    body = json.loads(value)
    return body

"""给整个数据集打好标签
"""
@router.post("/play/inference/dataset")
async def inference_dataset(inferenceDto: dto.CreateDatasetInferenceTaskDto,
                            pika_publisher = Depends(get_rabbitmq_blockingconnection),
                            user: entity.User = Depends(get_current_active_user),
                            db: Session = Depends(get_db)):
    # check if task belongs to current user.
    _ = await task_service.get_task_detail(inferenceDto.task_id, user.username, db)
    
    # 发送任务消息
    check_id = await task_service.start_inference_dataset(inferenceDto.model_id, inferenceDto.dataset_id, pika_publisher, db)
    return {"check_id": check_id}

@router.get("/play/dataset/{check_id}/check")
async def inference_dataset_check(check_id: str, request: Request):
    """异步接口，提交一个样本进行预测后，通过此接口查询模型推理结果
    """
    cache_key = "inferencedataset:{}".format(check_id)
    redis = request.app.state.redis#
    value = await redis.get(cache_key)

    if value is None:
        return {"state":"PENDING"}
    
    body_dict = json.loads(value)
    
    if "state" in body_dict and body_dict["state"] == "SUCCESS":
        zip_path = body_dict["zip_path"]
        #

    return body_dict

@router.get("/play/inference/download", response_class=FileResponse)
async def get_zip(file_path:str):
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path, media_type='application/zip')

    return FileResponse()