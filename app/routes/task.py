from fastapi import APIRouter, Depends, Request, HTTPException, Query
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import User
from app.crud.task import create_task, get_tasks_by_user, get_tasks, task_detail, update_task, delete_task, sort_tasks
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskSortOptions, PriorityEnum
from app.core.deps import get_current_user
from typing import List, Optional

router = APIRouter()


@router.post('/create')
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_task(db, current_user.id, task)


@router.get('/tasks-by-user', response_model=List[TaskRead])
async def task_by_user(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_tasks_by_user(db, current_user.id)


@router.get('/all', response_model=List[TaskRead])
async def all_tasks(db: AsyncSession = Depends(get_db)):
    return await get_tasks(db)



@router.get('/sort')
async def tasks_sort(
    status: Optional[TaskSortOptions] = Query(None), 
    priority: Optional[PriorityEnum] = Query(None), 
    db: AsyncSession = Depends(get_db)
):
    return await sort_tasks(db, status, priority)
    

@router.get('/{task_id}')
async def get_task_detail(task_id: int, db: AsyncSession = Depends(get_db)):
    return await task_detail(db, task_id)


@router.put('/{task_id}')
async def task_update(task_id: int, task: TaskUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_task(db, current_user.id, task_id, task)


@router.delete('/{task_id}')
async def task_delete(task_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_task(db, task_id)