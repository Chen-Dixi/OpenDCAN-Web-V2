import json
from datetime import datetime
from distutils.command.config import config
from typing import Optional, Any, List, Tuple
from unicodedata import name
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
    is_admin: bool

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

class PydanticSourceDatasetGetter(GetterDict):
    custom_keys = ['is_active']

    def get(self, key: str, default: Any) -> Any:
        if key == 'is_active':
            val = getattr(self._obj, key)
            return True if val == 1 else False
        elif key == 'labels':
            val = getattr(self._obj, key)
            if val is None:
                return []
            return json.loads(val)
        else:
            return getattr(self._obj, key, default)

class SourceDatasetRecordDto(BaseModel):
    id : int
    title : Optional[str]
    description : Optional[str]
    file_path : Optional[str]
    labels: List[str]
    label_num: int
    create_name : str
    update_name : str
    is_active : bool
    state : int
    
    class Config:
        orm_mode = True
        getter_dict = PydanticSourceDatasetGetter

class TargetDatasetRecordSelection(BaseModel):
    id: int
    title: Optional[str]

    class Config:
        orm_mode = True

class PydanticSourceRecordSelectionGetter(GetterDict):

    def get(self, key: str, default: Any) -> Any:
        if key == 'labels':
            val = getattr(self._obj, key)
            if val is None:
                return []
            labels =  json.loads(val)
            return [SourceDatasetRecordSelection.Label(name=item) for item in labels]

        else:
            return getattr(self._obj, key, default)


class SourceDatasetRecordSelection(BaseModel):
    class Label(BaseModel):
        name: str
    id: int
    title: Optional[str]
    labels: List[Label]

    class Config:
        orm_mode = True
        getter_dict = PydanticSourceRecordSelectionGetter

class CreateTargetDatasetRecord(BaseModel):
    title: str
    file_path : str
    username : str
    create_name : str

class UpdateDatasetRecord(BaseModel):
    id: int
    title: str
    description : Optional[str]

class CreateSourceDatasetRecordDto(BaseModel):
    title: str
    file_path : str
    create_name : str

class QueryTargetDatasetDto(BaseModel):
    limit: int
    offset: int
    username: str
    ipp: int

class QueryTargetDatasetResponse(BaseModel):
    datasets: Optional[List[TargetDatasetRecordDto]]
    maxPage: int

class QuerySourceDatasetResponse(BaseModel):
    datasets: Optional[List[SourceDatasetRecordDto]]
    maxPage: int

class QueryTargetDatasetSelectionResponse(BaseModel):
    selections: List[TargetDatasetRecordSelection]

class QuerySourceDatasetSelectionResponse(BaseModel):
    selections: List[SourceDatasetRecordSelection]

# ========================== task Record
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

class UpdateTaskDatasetConfigDto(BaseModel):
    task_id: int
    source_id: int
    source_name: str
    target_id: int
    target_name: str

class ModelRecordDto(BaseModel):
    """
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) DEFAULT NULL COMMENT '模型名称，文件名称',
  `task_id` int NOT NULL COMMENT '所属task id',
  `file_path` varchar(128) DEFAULT NULL COMMENT '文件在系统中的路径位置, 包含文件名',
  `model_type` tinyint DEFAULT NULL COMMENT '模型类型, 1 PyTorch 2 Tensorflow 暂时用不到',
  `state` tinyint NOT NULL DEFAULT '2' COMMENT '1: READY 2: TRAINING READY状态下才能被选择用于推理标注',
  `source_id` int DEFAULT NULL COMMENT '源域数据集id',
  `source_name` varchar(120) DEFAULT NULL COMMENT '源域数据集名称, 冗余字段',
  `target_id` int DEFAULT NULL COMMENT '目标域数据集id',
  `target_name` varchar(120) DEFAULT NULL COMMENT '目标域数据集名称, 冗余字段',
  `create_name` varchar(100) DEFAULT NULL COMMENT '上传数据集的人',
  `update_name` varchar(100) DEFAULT NULL COMMENT '更新数据集信息的人',
  `is_active` tinyint NOT NULL DEFAULT '0' COMMENT '1 active; 2 deleted',
  `create_time` bigint DEFAULT NULL,
  `update_time` bigint DEFAULT NULL,
  CONSTRAINT `pk_id` PRIMARY KEY (`id`),
  KEY `model_record_idx_task_id` (`task_id`) USING BTREE
    """
    id: int
    task_id: int
    username: str
    file_path: Optional[str]
    model_type: Optional[int]
    state: int  # 1: TRAINING 2: READY READY状态下才能被选择用于推理标注

    source_id : Optional[int]
    source_name : Optional[str]
    target_id : Optional[int]
    target_name : Optional[str]
    
    create_name : Optional[str]
    update_name : Optional[str]
    is_active : bool # 1 active; 2 disabled
    create_time : str
    update_time : str

    class Config:
        orm_mode = True
        getter_dict = PydanticTaskRecordGetter

class QueryTaskTrainResponse(BaseModel):
    trainings : List[ModelRecordDto]
    maxPage : int

class CreateTrainingTaskDto(BaseModel):
    task_id: int
    source_id: int
    source_name: str
    target_id: int
    target_name: str