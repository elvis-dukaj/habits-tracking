from typing import Optional
from fastapi import APIRouter, Query

from app.service import HabitsTrackingService
from app.schemas import HabitRead, HabitCreate


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
    def get_habits(user_id: Optional[int] = None, periodicity: Optional[int] = None, offset: int = 0,
                   limit: int = Query(default=100, lte=100)):
        if user_id is None:
            return habit_service.get_habits(offset, limit)

        if periodicity is None:
            return habit_service.get_habits_by_user_id(user_id, offset, limit)
        else:
            return habit_service.get_habits_by_user_and_periodicity(user_id, periodicity, offset, limit)

    @routers.get("/{habit_id}", response_model=HabitRead)
    def get_by_id(habit_id):
        return habit_service.get_habit_by_id(habit_id)

    @routers.delete("/{habit_id}")
    def delete(habit_id: int):
        habit_service.delete_habit(habit_id)

    return routers
