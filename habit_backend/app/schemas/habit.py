from typing import Optional
import datetime

from sqlmodel import SQLModel, Field


class HabitBase(SQLModel):
    user_id: int = Field(index=True, foreign_key="user.user_id")
    task: str
    periodicity: int
    created_at: datetime.date


class Habit(HabitBase, table=True):
    habit_id: Optional[int] = Field(default=None, primary_key=True)


class HabitCreate(HabitBase):
    pass


class HabitRead(HabitBase):
    habit_id: int
