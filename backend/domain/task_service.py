import os
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from fastapi import HTTPException, status, UploadFile
from mq.rabbitmq import PikaPublisher

from repository import entity, dto, crud
from settings import UPLOAD_IMAGE_EXTENSIONS, DATASET_UPLOAD_PATH

from common import utils

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

async def start_training(createDto: dto.CreateTrainingTaskDto, username: str, db: Session, pika_publisher: PikaPublisher)->int:
    db_model_record = crud.create_model_record(db, createDto.task_id, 
                             username, 
                             createDto.source_id, createDto.source_name,
                             createDto.target_id, createDto.target_name, auto_commit=False)
    # 更新任务状态，state=2 TRAINING
    now_time = datetime.now(timezone.utc)
    now_time = int(datetime.timestamp(now_time)*1000)
    crud.update_task_record_by_id(createDto.task_id, {"state": 2, "update_time":now_time, "update_name":username}, db, auto_commit=False)
    
    db_target = crud.get_target_dataset_record_by_id(db = db, recordId = createDto.target_id)
    db_source = crud.get_source_dataset_record_by_id(db = db, recordId = createDto.source_id)

    if (db_target is None) or (db_source is None) or (db_target.state != 1) or (db_source.state != 1):
        raise HTTPException(status_code=400, detail="Data not found")

    # 消息队列 提交一个 训练任务
    # mq_channel.basic_publish(exchange='dl_task', routing_key='train', body='Hello')
    mq_message = {
        'source_path': db_source.file_path,
        'target_path': db_target.file_path,
        'model_id': db_model_record.id,
        'task_id': createDto.task_id,
    }

    pika_publisher.send_training_task(mq_message)
    db.commit()
    return db_model_record.id

async def start_inference_single_sample(file: UploadFile, model_id: int, pika_publisher: PikaPublisher, db: Session):
    """
    用训练好的模型，预测一个图片样本
    1. 图片临时存储在文件系统中
    2. 把文件路径，模型文件路径通过消息中间件传递过去
    3. 返回一个uuid 给 前端，前端用这个uuid 不断询问fastapi 推理结果
    3. 推理结束后, 返回结果给FastAPI，写入redis里面。
    4. 推理完成后，此时前端向fastapi询问结果时，就能得到结果。
    """
    # 查询模型文件路径
    db_model = crud.get_active_model_record_by_id(model_id, db)
    if db_model is None:
        raise HTTPException(status_code=400, detail="Data not found")
    db_source = crud.get_source_dataset_record_by_id(db, db_model.source_id)
    source_dto = dto.SourceDatasetRecordDto.from_orm(db_source)

    # 获取源域数据集的信息，需要用到它的 classes
    if db_source is None:
        raise HTTPException(status_code=400, detail="Data not found")
    # 将图片作为临时文件保存
    content = await file.read()
    origin_filename = file.filename
    if not any(origin_filename.endswith(ext) for ext in UPLOAD_IMAGE_EXTENSIONS):
        raise HTTPException(status_code=400, detail="File is not an allowed extension.")
    suffix = origin_filename[origin_filename.index('.'):]
    
    uuid_id = utils.generateUUID()
    filename = uuid_id+'_'+origin_filename
    save_dir = os.path.join(DATASET_UPLOAD_PATH, 'tmp')
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    with open(save_path,'wb') as f:
        f.write(content)

    # 发送消息 给 runner-inference
    mq_message = {
        'sample_path': save_path,
        'classes': source_dto.labels,
        'model_path': db_model.file_path,
        'check_id': uuid_id,
    }
    pika_publisher.send_sample_label(mq_message)
    # 返回 uuid token 给前端，用这个uuid查询推理结果
    return uuid_id

async def get_ready_model_selections(task_id:int, username: str, db: Session):
    task_db = crud.get_task_record_by_id(db, task_id)
    if task_db.username != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access to data")
    
    selections = crud.get_ready_model_records_by_taskId(task_id, db)

    return [dto.ModelSelection.from_orm(selection) for selection in selections]

async def start_inference_dataset(model_id: int, dataset_id: int, pika_publisher: PikaPublisher, db: Session):
    db_target = crud.get_target_dataset_record_by_id(db = db, recordId = dataset_id)
    

    db_model = crud.get_active_model_record_by_id(model_id, db)
    if db_model is None:
        raise HTTPException(status_code=400, detail="Data not found")
    if db_model.state != 1:
        raise HTTPException(status_code=400, detail="Model not ready")
    db_source = crud.get_source_dataset_record_by_id(db, db_model.source_id)
    source_dto = dto.SourceDatasetRecordDto.from_orm(db_source)
    
    uuid_id = utils.generateUUID()

    mq_message = {
        'target_path': db_target.file_path,
        'classes': source_dto.labels,
        'model_path': db_model.file_path,
        'model_id': model_id,
        'check_id': uuid_id,
    }

    pika_publisher.send_dataset_label(mq_message)
    
    return uuid_id