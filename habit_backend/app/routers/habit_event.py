import datetime
from typing import Optional
import datetime

from fastapi import APIRouter

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

    @routers.get("/{habit_event_id}", response_model=HabitEventRead)
    def get_habit_event_by_id(habit_event_id: int):
        return habit_service.get_habit_event_by_id(habit_event_id)

    return routers
