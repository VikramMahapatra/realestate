
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: str
    is_active: bool
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
