import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class HabitEventBase(SQLModel):
    user_id: int = Field(foreign_key="user.user_id")
    habit_id: int = Field(foreign_key="habit.habit_id")
    completed_at: Optional[datetime.date]  # = Field(default_factory=datetime.date.today)


class HabitEvent(HabitEventBase, table=True):
    habit_event_id: int = Field(default=None, primary_key=True)


class HabitEventComplete(HabitEventBase):
    pass


class HabitEventRead(HabitEventBase):
    pass
