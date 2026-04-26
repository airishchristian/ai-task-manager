# app/models/summary.py
from sqlmodel import SQLModel, Field
from datetime import datetime

class Summary(SQLModel, table=True):
    # TODO: What fields does a weekly summary record need?
    # Hint: id, the summary text itself, when was it created, which user does it belong to?
    # id          → primary key, optional int
    # content     → str (the AI-generated summary text)
    # created_at  → datetime, default to now
    #               Hint: Field(default_factory=datetime.utcnow)
    # user_id     → int | None, foreign key to "user.id"
    id: int | None = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: int | None = Field(foreign_key="user.id")
