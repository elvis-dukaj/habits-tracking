from fastapi import APIRouter

from service.habit import HabitsTrackingService
from schemas.habits import User, CreateUserResponse


def create_user_routers() -> APIRouter:
    user_routers = APIRouter(
        prefix="/habits_tracking/user",
        tags=["user"]
    )

    habit_service = HabitsTrackingService()

    @user_routers.post("/", response_model=CreateUserResponse, status_code=201)
    def create_user(user: User):
        response = habit_service.create_user(user)
        return response

    @user_routers.get("/get_by_id/{user_id}", response_model=User)
    def get_user_by_id(user_id: int):
        user_response = habit_service.get_user_info_by_id(user_id)
        return user_response

    @user_routers.get("/get_by_username/{username}", response_model=User)
    def get_user_by_username(username: str):
        user_response = habit_service.get_user_info_by_username(username)
        return user_response

    @user_routers.delete("/{user_id}")
    def delete_user(user_id: int):
        habit_service.delete_user(user_id)

    return user_routers
