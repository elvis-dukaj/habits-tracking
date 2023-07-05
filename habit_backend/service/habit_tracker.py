from schemas.user import User
from schemas.habit import Habit
from schemas.habit_event import HabitEvent

from db.client import DatabaseClient


class HabitsTrackingService:
    def __init__(self, db: DatabaseClient):
        self._db = db

    def create_user(self, user: User) -> User:
        full_user = self._db.add_user(user)
        return full_user

    def delete_user(self, user_id: int) -> None:
        self._db.delete_user(user_id)

    def get_user_by_id(self, user_id: int) -> User:
        user = self._db.get_user_by_id(user_id)
        return user

    def get_user_by_username(self, username: str) -> User:
        user = self._db.get_user_by_username(username)
        return user

    def create_habit(self, habit: Habit):
        habit = self._db.create_habit(habit)
        return habit

    def delete_habit(self, habit_id: int) -> None:
        self._db.delete_habit(habit_id)

    def get_habit_by_id(self, habit_id: int) -> Habit:
        habit = self._db.get_habit_by_id(habit_id)
        return habit

    def get_all_habits(self) -> list[Habit]:
        habits = self._db.get_all_habits()
        return habits

    def get_habits_by_user_id(self, user_id: int) -> list[Habit]:
        reply = self._db.get_habits_by_user_id(user_id)
        return reply

    def mark_habit_completed(self, user_id: int, habit_id: int) -> HabitEvent:
        event = self._db.add_habit_event(user_id, habit_id)
        return event
