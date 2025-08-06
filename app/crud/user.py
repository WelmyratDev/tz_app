from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from app.models.base import User
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest
from passlib.context import CryptContext
from app.core.security import create_access_token, create_refresh_token
from fastapi import HTTPException


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(real_password: str, hashed_password: str):
    return pwd_context.verify(real_password, hashed_password)


async def create_user(db: AsyncSession, user: UserCreate):
    if not user.email and user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    db_user = await db.execute(select(User).where(User.email == user.email))
    existing_user = db_user.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

    

async def get_users(db: AsyncSession):
    db_users = await db.execute(select(User))
    return db_users.scalars().all()



    