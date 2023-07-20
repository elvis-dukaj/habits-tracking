import datetime

from pydantic import BaseModel


class HabitEvent(BaseModel):
    user_id: int
    habit_id: int
    completed_at: datetime.date
