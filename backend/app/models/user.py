# app/models/user.py

from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    # TODO: Define these fields:
    #
    # id             → Optional[int], primary_key=True, default None
    # name           → str, required
    # email          → str, required  (we'll add uniqueness in Lesson 7)
    # hashed_password → str, required  (we'll fill this in Lesson 7)
    id : int | None = Field(default=None, primary_key=True)
    name: str 
    email: str
    hashed_password: str