from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.base import User
from app.schemas.auth import LoginRequest, RefreshRequest
from app.core.security import create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
from fastapi import HTTPException
from .user import verify_password
from jose import JWTError, jwt


async def login_user(db: AsyncSession, data: LoginRequest):
    db_user = await db.execute(select(User).where(User.email == data.email))
    user = db_user.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Error email or password")
    
    access_token = create_access_token(data={'sub': str(user.id)})
    refresh_token = create_refresh_token(data={'sub': str(user.id)})

    context = {'access_token': access_token, 'refresh_token': refresh_token}
    return context


async def refresh_token_auth(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=401, detail="error token")
    except JWTError:
        raise HTTPException(status_code=401, detail="error token")
    
    access_token = create_access_token(data={'sub': user_id})
    refresh_token = create_refresh_token(data={'sub': user_id})

    context = {'access_token': access_token, 'refresh_token': refresh_token}
    return context
        