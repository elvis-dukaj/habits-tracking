import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str


class User(UserBase, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    user_id: int

