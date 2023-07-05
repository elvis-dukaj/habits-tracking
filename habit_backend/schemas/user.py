import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    user_id: Optional[int]
    created_at: Optional[datetime.date]
    username: str
    email: str

