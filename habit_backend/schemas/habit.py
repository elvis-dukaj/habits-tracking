from pydantic import BaseModel


class Habit(BaseModel):
    task: str
    description: str
    periodicity: int


class MultipleHabitResponse(BaseModel):
    users: list[Habit]


class CreateHabitResponse(BaseModel):
    id: int


class HabitResponse(BaseModel):
    id: int
    task: str
    description: str
    periodicity: str
