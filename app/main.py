from fastapi import FastAPI
from app.routes import user as users_router
from app.routes import auth as auth_router
from app.routes import task as task_router

app = FastAPI(title="Task Management System", description="New service for users ))", version="1.0.0")


app.include_router(users_router.router, tags=['Users'])
app.include_router(auth_router.router, prefix="/auth", tags=['Auth'])
app.include_router(task_router.router, prefix="/task", tags=['Tasks'])
