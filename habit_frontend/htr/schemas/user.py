from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    username: str


class UserCreateResponse(BaseModel):
    user_id: int
    username: str
