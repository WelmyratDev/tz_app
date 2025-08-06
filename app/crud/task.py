from sqlalchemy import select, and_, desc, asc
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskCreate, TaskUpdate, TaskSortOptions, PriorityEnum
from app.models.base import Task



async def create_task(db: AsyncSession, user_id: int, task: TaskCreate):
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    if not task.title and not task.description:
        raise HTTPException(status_code=400, detail="Title and description are required")
    
    new_task = Task(user_id=user_id, title=task.title, description=task.description, is_completed=task.is_completed, priority=task.priority)
    
    db_task = await db.execute(select(Task).where(
        and_(
            Task.user_id == user_id,
            Task.title == task.title
        )
    ))
    existing_task = db_task.scalar_one_or_none()
    if existing_task:
        raise HTTPException(status_code=400, detail="This task with this user already exists")
    
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def get_tasks_by_user(db: AsyncSession, user_id: int):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    db_tasks = await db.execute(select(Task).where(Task.user_id == user_id))
    return db_tasks.scalars().all()


async def get_tasks(db: AsyncSession):
    tasks = await db.execute(select(Task))
    return tasks.scalars().all()


async def task_detail(db: AsyncSession, task_id: int):
    db_task = await db.execute(select(Task).where(Task.id == task_id))
    result = db_task.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Task Not found")
    return result


async def update_task(db: AsyncSession, user_id: int, task_id: int, task: TaskUpdate):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    db_task = await db.execute(select(Task).where(Task.id == task_id))
    result = db_task.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Task Not found")
    
    if task.title is not None:
        result.title = task.title
    if task.description is not None:
        result.description = task.description
    if task.is_completed is not None:
        result.is_completed = task.is_completed
    if task.priority is not None:
        result.priority = task.priority

    await db.commit()
    await db.refresh(result)
    return result


async def delete_task(db: AsyncSession, task_id: int):
    db_task = await db.execute(select(Task).where(Task.id == task_id))
    get_task = db_task.scalar_one_or_none()
    if get_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(get_task)
    await db.commit()
    return get_task


async def sort_tasks(db: AsyncSession, options: TaskSortOptions, priority: PriorityEnum):
    #if user_id is None:
        #raise HTTPException(status_code=401, detail="Not Authenticated")

    if options and priority:
        db_tasks = await db.execute(select(Task).where(
            and_(
                Task.is_completed == (True if options.value == "done" else False),
                Task.priority == priority.value
            )
        ))
    elif priority:
        db_tasks = await db.execute(select(Task).where(
            Task.priority == priority.value
        ))
    elif options:
        db_tasks = await db.execute(select(Task).where(
            Task.is_completed == (True if options.value == "done" else False)
        ))
    else:
        raise HTTPException(status_code=400, detail="Params not selected")
    
    return db_tasks.scalars().all()