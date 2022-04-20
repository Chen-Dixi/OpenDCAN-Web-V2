from datetime import datetime
from distutils.command.config import config
from typing import Optional, Any, List
from pydantic import BaseModel
from pydantic.utils import GetterDict
from uvicorn import Config
class UserBaseDTO(BaseModel):
    email: str
    username: str
    display_name: str

class PydanticUserGetter(GetterDict):
    custom_keys = ['is_active']

    def get(self, key: str, default: Any) -> Any:
        if key == 'is_active':
            val = getattr(self._obj, key)
            return True if val == 1 else False
        elif key == 'is_admin':
            val = getattr(self._obj, 'user_type')
            return True if val == 1 else False
        else:
            return getattr(self._obj, key, default)

        
class UserDTO(UserBaseDTO):
    id: int
    is_active: bool
    is_admin: bool
    class Config:
        orm_mode = True
        getter_dict = PydanticUserGetter

class CreateUserDTO(UserBaseDTO):
    password: str
    user_type: int


class Token(BaseModel):
    access_token: str
    username: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# ========================== Dataset Record

class PydanticTargetDatasetGetter(GetterDict):
    custom_keys = ['is_active']

    def get(self, key: str, default: Any) -> Any:
        if key == 'is_active':
            val = getattr(self._obj, key)
            return True if val == 1 else False
        else:
            return getattr(self._obj, key, default)
class TargetDatasetRecordDto(BaseModel):
    id : int
    title : Optional[str]
    description : Optional[str]
    username : str
    file_path : Optional[str]
    create_name : str
    update_name : str
    is_active : bool
    state : int
    
    class Config:
        orm_mode = True
        getter_dict = PydanticTargetDatasetGetter

class TargetDatasetRecordSelection(BaseModel):
    id: int
    title: Optional[str]

    class Config:
        orm_mode = True

class CreateTargetDatasetRecord(BaseModel):
    title: str
    file_path : str
    username : str
    create_name : str

class QueryTargetDatasetDto(BaseModel):
    limit: int
    offset: int
    username: str
    ipp: int

class QueryTargetDatasetResponse(BaseModel):
    datasets: Optional[List[TargetDatasetRecordDto]]
    maxPage: int

class QueryTargetDatasetSelectionResponse(BaseModel):
    selections: List[TargetDatasetRecordSelection]

class PydanticTaskRecordGetter(GetterDict):
    date_keys = ['create_time', 'update_time']

    def get(self, key: str, default: Any) -> Any:
        if key == 'is_active':
            val = getattr(self._obj, key)
            return True if val == 1 else False
        elif key in self.date_keys:
            val = getattr(self._obj, key)
            # 【13位毫秒精度数字】转换成【时间戳】
            return datetime.fromtimestamp(val//1000).strftime("%Y-%m-%d")
        else:
            return getattr(self._obj, key, default)

class TaskRecordDto(BaseModel):
    id : int
    name : str
    username : str
    state : int  # 1 ready, 2 not ready
    source_id : Optional[int]
    source_name : Optional[str]
    target_id : Optional[int]
    target_name : Optional[str]

    is_active : bool # 1 active; 2 disabled
    create_time : str
    update_time : str

    class Config:
        orm_mode = True
        getter_dict = PydanticTaskRecordGetter

class QueryTaskRecordResponse(BaseModel):
    tasks: Optional[List[TaskRecordDto]]
    maxPage: int

class CreateTaskDto(BaseModel):
    task_name: str