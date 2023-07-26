from fastapi import APIRouter

from app.service.habit_tracker import HabitsTrackingService
from app.schemas import UserCreate, UserRead


def create_user_routers(habit_service: HabitsTrackingService) -> APIRouter:
    routers = APIRouter(
        prefix="/user",
        tags=["user"],
    )

    @routers.post("/", response_model=UserRead, status_code=201)
    def create(user: UserCreate):
        response = habit_service.create_user(user)
        return response

    @routers.get("/id/{user_id}", response_model=UserRead)
    def get_by_id(user_id: int):
        user_response = habit_service.get_user_by_id(user_id)
        return user_response

    @routers.get("/username/{username}", response_model=UserRead)
    def get_by_username(username: str):
        user_response = habit_service.get_user_by_username(username)
        return user_response

    @routers.delete("/{user_id}")
    def delete(user_id: int):
        habit_service.delete_user(user_id)

    return routers
