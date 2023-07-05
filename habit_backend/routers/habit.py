from fastapi import APIRouter

from service.habit_tracker import HabitsTrackingService
from schemas.habit import Habit


def create_habit_routers(habit_service: HabitsTrackingService) -> APIRouter:
    routers = APIRouter(
        prefix="/habit",
        tags=["habit_event"]
    )

    @routers.post("/", response_model=Habit, status_code=201)
    def create(habit: Habit):
        response = habit_service.create_habit(habit)
        return response

    @routers.get("/get_by_id/all", response_model=list[Habit])
    def get_all():
        response = habit_service.get_all_habits()
        return response

    @routers.get("/get_by_id/{habit_id}", response_model=Habit)
    def get_by_id(habit_id: int):
        response = habit_service.get_habit_by_id(habit_id)
        return response

    @routers.get("/get_by_user_id/{user_id}", response_model=list[Habit])
    def get_by_user_id(user_id: int):
        reply = habit_service.get_habits_by_user_id(user_id)
        return reply

    @routers.delete("/{habit_id}")
    def delete(habit_id: int):
        habit_service.delete_habit(habit_id)

    return routers
