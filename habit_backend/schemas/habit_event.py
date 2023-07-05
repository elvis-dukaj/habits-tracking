import datetime
from typing import Optional
from pydantic import BaseModel


class HabitEvent(BaseModel):
    event_id: Optional[int]
    user_id: int
    habit_id: int
    completed_at: datetime.date
