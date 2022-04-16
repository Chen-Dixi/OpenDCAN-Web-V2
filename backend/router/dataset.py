from typing import List
from os import path
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session


from domain.model import User
from dependencies import get_current_active_user, get_db, pwd_context
from repository.database import SessionLocal
from repository import dto, entity, crud
from common import utils
from settings import dataset_upload_path
router = APIRouter(
    prefix="/dataset",
    tags=["dataset"]
)

@router.post("/target/upload")
async def uplaod_target_dataset(file: UploadFile, user: entity.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
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
    
    # db_user = crud.get_user_by_email(db, user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    # db_user = crud.get_user_by_username(db, user.username)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Username already registered")
    # # automatically orm
    # user.password = pwd_context.hash(user.password)
    # return crud.create_user(db, user)
    content = await file.read()
    filename = file.filename
    
    suffix = filename[filename.index('.'):]
    
    filename = utils.generateUUID()+suffix
    save_path = path.join(dataset_upload_path, 'target_dataset', filename)
    with open(save_path,'wb') as f:
        f.write(content)
    
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