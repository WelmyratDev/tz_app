from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
 

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=settings.DEBUG)


# Это тоже вариант
# async_session = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

asc_sessionmaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def get_db():
    async with asc_sessionmaker() as session:
        yield session