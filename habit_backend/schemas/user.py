from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str


class CreateUserResponse(BaseModel):
    user_id: int
