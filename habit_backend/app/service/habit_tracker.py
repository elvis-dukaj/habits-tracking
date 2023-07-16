from typing import Optional
import datetime

from app.schemas.user import UserCreate, UserRead
from app.schemas.habit import HabitCreate, HabitRead
from app.schemas.habit_event import HabitEventComplete
from app.db.client import DatabaseClient


class HabitsTrackingService:
    def __init__(self, db: DatabaseClient):
        self._db = db

    def create_user(self, user: UserCreate) -> UserRead:
        response = self._db.add_user(user)
        return response

    def delete_user(self, user_id: int) -> None:
        self._db.delete_user(user_id)

    def get_user_by_id(self, user_id: int) -> UserRead:
        user = self._db.get_user_by_id(user_id)
        return user

    def get_user_by_username(self, username: str) -> UserRead:
        user = self._db.get_user_by_username(username)
        return user

    def create_habit(self, habit: HabitCreate) -> HabitRead:
        habit = self._db.create_habit(habit)
        return habit

    def delete_habit(self, habit_id: int) -> None:
        self._db.delete_habit(habit_id)

    def get_habit_by_id(self, habit_id) -> HabitRead:
        habit = self._db.get_habit_by_id(habit_id)
        return habit

    def get_habits(self, offset: int, limit: int) -> list[HabitRead]:
        habits = self._db.get_habits(offset, limit)
        return habits

    def get_habits_by_user_id(self, user_id: int, offset: int, limit: int) -> list[HabitRead]:
        reply = self._db.get_habits_by_user_id(user_id, offset, limit)
        return reply

    def get_habits_by_periodicity(self, periodicity: int, offset: int, limit: int) -> list[HabitRead]:
        reply = self._db.get_habits_by_periodicity(periodicity, offset, limit)
        return reply

    def mark_habit_completed(self, habit_event: HabitEventComplete):
        event = self._db.add_habit_event(habit_event)
        return event

    def get_habit_event_by_id(self, habit_event_id: int):
        return self._db.get_habit_event_by_id(habit_event_id)

    def get_habit_event_by_user_id(self, user_id: int, offset: int, limit: int):
        return self._db.get_habit_event_by_user_and_habit(user_id, offset, limit)

    def get_habit_event_by_user_and_habit(self, user_id: int, habit_id: int, offset: int, limit: int):
        return self._db.get_habit_event_by_user_and_habit(user_id, habit_id, offset, limit)
