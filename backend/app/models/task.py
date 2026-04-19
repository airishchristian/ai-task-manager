from sqlmodel import SQLModel, Field
from datetime import date
from app.schemas.task import Priority, Status


class Task(SQLModel, table=True):
    # TODO: Define these fields:
    #
    # id          → Optional[int], primary_key=True, default None
    # title       → str, required
    # description → Optional[str], default None
    # priority    → Priority, default Priority.LOW
    # status      → Status, default Status.PENDING
    # due_date    → Optional[date], default None
    id: int | None = Field(default=None, primary_key=True)
    title: str 
    description: str | None = None
    priority: Priority = Priority.LOW
    status: Status = Status.PENDING
    due_date: date | None = None 
    user_id: int | None = Field(default=None, foreign_key="user.id")