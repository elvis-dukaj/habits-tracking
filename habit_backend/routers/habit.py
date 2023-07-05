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
        response = habit_service.create_habit(habit)
        return response

    @routers.get("/get_by_id/all", response_model=MultipleHabitResponse)
    def get_all():
        response = habit_service.get_all_habits()
        return response

    @routers.get("/get_by_id/{id}", response_model=Habit)
    def get_by_id(id: int):
        response = habit_service.get_habit_by_id(id)
        return response

    @routers.get("/get_by_user_id/{user_id}", response_model=MultipleHabitResponse)
    def get_by_user_id(user_id: int):
        reply = habit_service.get_habits_by_user_id(user_id)
        return reply

    @routers.delete("/{id}")
    def delete(id: int):
        habit_service.delete_habit(id)

    return routers
