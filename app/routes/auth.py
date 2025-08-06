from fastapi import APIRouter, Depends, Request, HTTPException
from app.crud.user import create_user
from app.crud.auth import login_user, refresh_token_auth
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import TokenResponse, RefreshRequest, LoginRequest
from app.schemas.user import UserCreate
from app.models.base import User
from app.core.deps import get_current_user
from .user import UserRead


router = APIRouter()


@router.post('/register')
async def auth_register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)



@router.post('/login', response_model=TokenResponse)
async def auth_login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login_user(db, data)

@router.post('/refresh', response_model=TokenResponse)
async def refresh_token(data: RefreshRequest):
    return await refresh_token_auth(data.refresh_token)


@router.get('/me', response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user