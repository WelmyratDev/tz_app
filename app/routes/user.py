from fastapi import APIRouter, Depends
from app.crud.user import create_user, get_users
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserRead
from typing import List

router = APIRouter()


@router.get('/users', response_model=List[UserRead])
async def all_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)