from fastapi import APIRouter

from service.habit import HabitsTrackingService
from schemas.habits import User, CreateUserResponse


def create_habits_routers() -> APIRouter:
    user_routers = APIRouter(
        prefix="/habits_tracking",
        tags=["user"]
    )

    habit_service = HabitsTrackingService()

    @user_routers.post("/", response_model=CreateUserResponse, status_code=201)
    def create_user(user: User):
        response = habit_service.create_user(user)
        return response

    @user_routers.get("/user/{user_id}", response_model=User)
    def get_user_by_id(user_id: int):
        user_response = habit_service.get_user_info(user_id)
        return user_response

    return user_routers
