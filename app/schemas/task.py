from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime



class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False
    priority: Optional[PriorityEnum]


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = False
    priority: Optional[PriorityEnum] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False
    priority: Optional[PriorityEnum] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskSortOptions(str, Enum):
    done = "done"
    pending = "pending"
