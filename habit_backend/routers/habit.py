from fastapi import APIRouter

from service.habit import HabitsTrackingService
from schemas.habit import Habit, CreateHabitResponse, MultipleHabitResponse


def create_habit_routers(habit_service: HabitsTrackingService) -> APIRouter:
    routers = APIRouter(
        prefix="/habit",
        tags=["habit"]
    )

    @routers.post("/", response_model=CreateHabitResponse, status_code=201)
    def create(habit: Habit):
        # response = habit_service.create_user(user.py)
        # return response
        response = CreateHabitResponse()
        return response

    @routers.get("/get_by_id/{id}", response_model=Habit)
    def get_by_id(id: int):
        # user_response = habit_service.get_user_info_by_id(user_id)
        # return user_response

        pass

    @routers.get("/get_by_user_id/{user_id}", response_model=MultipleHabitResponse)
    def get_by_user_id(user_id: int):
        pass

    @routers.delete("/{id}")
    def delete(id: int):
        # habit_service.delete_user(user_id)
        pass

    return routers
