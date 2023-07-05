from pydantic import BaseModel


class Habit(BaseModel):
    user_id: int
    task: str
    description: str
    periodicity: int


class CreateHabitResponse(BaseModel):
    id: int
