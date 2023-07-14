from typing import Optional
from fastapi import APIRouter, Query

from app.service.habit_tracker import HabitsTrackingService
from app.schemas.habit import HabitRead, HabitCreate


def create_habit_routers(habit_service: HabitsTrackingService) -> APIRouter:
    routers = APIRouter(
        prefix="/habit",
        tags=["habit"]
    )

    @routers.post("/", response_model=HabitRead, status_code=201)
    def create(habit: HabitCreate):
        response = habit_service.create_habit(habit)
        return response

    @routers.get("/", response_model=list[HabitRead])
    def get_habits(user_id: Optional[int] = None, offset: int = 0, limit: int = Query(default=100, lte=100)):
        if user_id is None:
            return habit_service.get_habits(offset, limit)
        else:
            return habit_service.get_habits_by_user_id(user_id, offset, limit)

    @routers.get("/{habit_id}", response_model=HabitRead)
    def get_by_id(habit_id):
        return habit_service.get_habit_by_id(habit_id)

    @routers.get("/by_periodicity/{periodicity}", response_model=list[HabitRead])
    def get_habits_by_periodicity(periodicity: int, offset: int = 0, limit: int = Query(default=100, lte=100)):
        return habit_service.get_habits_by_periodicity(periodicity, offset, limit)

    @routers.delete("/{habit_id}")
    def delete(habit_id: int):
        habit_service.delete_habit(habit_id)

    return routers
