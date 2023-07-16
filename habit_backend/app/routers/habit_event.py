from typing import Optional
from fastapi import APIRouter, Query

from app.service.habit_tracker import HabitsTrackingService
from app.schemas.habit_event import HabitEventComplete, HabitEventRead


def create_habit_event_routers(habit_service: HabitsTrackingService) -> APIRouter:
    routers = APIRouter(
        prefix="/habit_event",
        tags=["habit_event"]
    )

    @routers.post("/", status_code=201)
    def mark_habit_completed(habit_event: HabitEventComplete):
        habit_service.mark_habit_completed(habit_event)

    @routers.get("/id/{habit_event_id}", response_model=HabitEventRead)
    def get_habit_event_by_id(habit_event_id: int):
        return habit_service.get_habit_event_by_id(habit_event_id)

    @routers.get("/", response_model=list[HabitEventRead])
    def get_habit_event_by_user_and_habit(user_id: int, habit_id: Optional[int] = None, offset: int = 0,
                                          limit: int = Query(default=100, lte=100)):
        if habit_id is None:
            return habit_service.get_habits_by_user_id(user_id, offset, limit)
        else:
            return habit_service.get_habit_event_by_user_and_habit(user_id, habit_id, offset, limit)

    return routers
