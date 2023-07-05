from fastapi import APIRouter

from service.habit import HabitsTrackingService
from schemas.user import User, CreateUserResponse


def create_user_routers(habit_service: HabitsTrackingService) -> APIRouter:
    routers = APIRouter(
        prefix="/user",
        tags=["user"],
    )

    @routers.post("/", response_model=CreateUserResponse, status_code=201)
    def create(user: User):
        response = habit_service.create_user(user)
        return response

    @routers.get("/get_by_id/{id}", response_model=User)
    def get_by_id(id: int):
        user_response = habit_service.get_user_info_by_id(id)
        return user_response

    @routers.get("/get_by_username/{username}", response_model=User)
    def get_by_username(username: str):
        user_response = habit_service.get_user_info_by_username(username)
        return user_response

    @routers.delete("/{id}")
    def delete(id: int):
        habit_service.delete_user(id)

    return routers
