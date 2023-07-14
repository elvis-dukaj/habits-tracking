from fastapi import APIRouter

from app.service.habit_tracker import HabitsTrackingService
from app.schemas.habit_event import HabitEvent


def create_habit_event_routers(habit_service: HabitsTrackingService) -> APIRouter:
    routers = APIRouter(
        prefix="/habit_event",
        tags=["habit_event"]
    )

    @routers.post("/complete/{user_id}/{habit_id}", response_model=HabitEvent, status_code=201)
    def mark_habit_completed(user_id: int, habit_id: int):
        reply = habit_service.mark_habit_completed(user_id, habit_id)
        return reply

    return routers
