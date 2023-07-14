import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    # created_at: Optional[datetime.date]
    username: str
    email: str


# class User(SQLModel, table=True):
#     user_id: Optional[int] = Field(default=None, primary_key=True)
#     # created_at: Optional[datetime.date]
#     username: str
#     email: str

# class UserRequest(BaseModel):
#     user_id: Optional[int]
#     username: str = Field(max_length=16)
#     email: str
#
#
# class CreateUserResponse(BaseModel):
#     user_id: int
