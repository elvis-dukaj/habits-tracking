from pydantic import BaseModel


class Habit(BaseModel):
    user_id: int
    task: str
    description: str
    periodicity: int


class CreateHabitResponse(BaseModel):
    id: int


# class HabitResponse(BaseModel):
#     id: int
#     user_id: int
#     task: str
#     description: str
#     periodicity: str


# class MultipleHabitResponse(BaseModel):
#     habits: list[Habit]
