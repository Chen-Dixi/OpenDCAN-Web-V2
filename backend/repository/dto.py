from typing import Optional, Any, List
from pydantic import BaseModel
from pydantic.utils import GetterDict
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
class TargetDatasetDto(BaseModel):
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

class CreateTargetDatasetRecord(BaseModel):
    file_path : str
    username : str
    create_name : str

class QueryTargetDatasetDto(BaseModel):
    limit: int
    offset: int
    username: str
    ipp: int

class QueryTargetDatasetResponse(BaseModel):
    datasets: Optional[List[TargetDatasetDto]]
    maxPage: int