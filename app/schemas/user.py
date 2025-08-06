from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)