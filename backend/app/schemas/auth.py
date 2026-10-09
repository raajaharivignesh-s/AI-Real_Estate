from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.db.models import RoleEnum

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: RoleEnum
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
