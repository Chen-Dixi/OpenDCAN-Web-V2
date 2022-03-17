from enum import Enum
from typing import Optional
from pydantic import BaseModel

class UserType(Enum):
    ADMIN = 0
    USER = 1
    
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str
    user_type: Optional[UserType] = None
    create_time: Optional[int] = None
    update_time: Optional[int] = None

# Security===========================
# Pydantic Model that will be used in the token endpoint for the response.
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None