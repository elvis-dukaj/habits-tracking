import datetime
from typing import Optional
from pydantic import BaseModel


class Habit(BaseModel):
    habit_id: Optional[int]
    created_at: Optional[datetime.date]
    user_id: int
    task: str
    description: str
    periodicity: int
