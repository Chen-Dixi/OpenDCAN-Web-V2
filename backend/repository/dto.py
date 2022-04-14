from typing import Optional
from pydantic import BaseModel

class UserBaseDTO(BaseModel):
    email: str
    username: str
    display_name: str

class UserDTO(UserBaseDTO):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True

class CreateUserDTO(UserBaseDTO):
    password: str
    user_type: int


class Token(BaseModel):
    access_token: str
    username: int
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None