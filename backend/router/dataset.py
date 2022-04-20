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
def uplaod_source_dataset(file: UploadFile, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    上传压缩后的数据集
    1. 解压
    2. 重命名 带uuid
    3. 更新数据库 表 target_dataset_record
    4. 返回
    """
    
    # db_user = crud.get_user_by_email(db, user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    # db_user = crud.get_user_by_username(db, user.username)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Username already registered")
    # # automatically orm
    # user.password = pwd_context.hash(user.password)
    # return crud.create_user(db, user)

    return {"filename": file.filename}


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

@router.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/dataset/target/upload" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)