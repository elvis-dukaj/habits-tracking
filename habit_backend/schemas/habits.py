from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str


class Habit(BaseModel):
    task: str
    periodicity: int


class MultipleUserResponse(BaseModel):
    users: list[User]


class CreateUserResponse(BaseModel):
    user_id: int


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
