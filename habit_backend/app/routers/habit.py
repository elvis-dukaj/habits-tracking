from fastapi import APIRouter, Query

from app.service.habit_tracker import HabitsTrackingService
from app.schemas.habit import HabitRead, HabitCreate


def create_habit_routers(habit_service: HabitsTrackingService) -> APIRouter:
    routers = APIRouter(
        prefix="/habit",
        tags=["habit_event"]
    )

    @routers.post("/", response_model=HabitRead, status_code=201)
    def create(habit: HabitCreate):
        response = habit_service.create_habit(habit)
        return response

    @routers.get("/get_by_id/", response_model=list[HabitRead])
    def get_all():
        response = habit_service.get_all_habits()
        return response

    @routers.get("/get_by_id/{habit_id}", response_model=HabitRead)
    def get_by_id(habit_id: int, offset: int = 0, limit: int = Query(default=100, lte=100)):
        response = habit_service.get_habit_by_id(habit_id, offset, limit)
        return response

    @routers.get("/get_by_user_id/{user_id}", response_model=list[HabitRead])
    def get_by_user_id(user_id: int, offset: int = 0, limit: int = Query(default=100, lte=100)):
        reply = habit_service.get_habits_by_user_id(user_id)
        return reply

    @routers.delete("/{habit_id}")
    def delete(habit_id: int):
        habit_service.delete_habit(habit_id)

    return routers
