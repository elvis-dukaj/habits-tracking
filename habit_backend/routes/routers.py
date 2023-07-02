from fastapi import APIRouter

from habit_backend.service.habit import HabitsTrackingService
from habit_backend.schemas.habits import UserResponse


def create_user_routers() -> APIRouter:
    user_routers = APIRouter(
        prefix="/habit_tracking"
    )

    habit_service = HabitsTrackingService

    @user_routers.get("/user/{user_id}", response_model=UserResponse)
    def get_user_by_id(user_id: int):
        user_response = habit_service.get_user_info(user_id)
        return user_response

    return user_routers
