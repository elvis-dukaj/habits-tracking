import datetime

from pydantic import BaseModel


class Habit(BaseModel):
    user_id: int
    habit_id: int
    task: str
    periodicity: int
    created_at: datetime.date
