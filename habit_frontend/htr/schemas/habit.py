import datetime

from pydantic import BaseModel


class Habit(BaseModel):
    user_id: int
    habit_id: int
    task: str
    periodicity: int


class HabitEvent(BaseModel):
    user_id: int
    habit_id: int
    completed_at: datetime.date
    habit_event_id: int
