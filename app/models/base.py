import sqlalchemy as db
from app.db.base import Base
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.schemas.task import PriorityEnum
from datetime import datetime, UTC


class User(Base):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))

    tasks = relationship("Task", back_populates="user", cascade="all,delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', created_at={self.created_at})>"


class Task(Base):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False, server_default=db.text("false"))
    priority = db.Column(SQLEnum(PriorityEnum), default=PriorityEnum.low)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', is_completed={self.is_completed})>"
