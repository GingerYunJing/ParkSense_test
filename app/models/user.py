from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
    email: EmailStr
    roles: List[str]
    is_active: bool = True
    mfa_enabled: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(User):
    hashed_password: str

class UserUpdate(BaseModel):
    roles: Optional[List[str]] = None
    is_active: Optional[bool] = None
    mfa_enabled: Optional[bool] = None
    class Config:
        title = "User Update" 