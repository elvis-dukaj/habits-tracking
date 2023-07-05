from schemas.user import (
    User,
    CreateUserResponse
)
from schemas.habit import (
    Habit,
    CreateHabitResponse,
)
from exception import UserNotFoundError
from db.client import DatabaseClient


class HabitsTrackingService:
    def __init__(self, db: DatabaseClient):
        self._db = db

    def create_user(self, user: User) -> CreateUserResponse:
        user_id = self._db.add_user(user)
        return CreateUserResponse(user_id=user_id)

    def delete_user(self, user_id: int) -> None:
        self._db.delete_user(user_id)

    def get_user_by_id(self, user_id: int) -> User:
        user = self._db.get_user_by_id(user_id)
        return user

    def get_user_by_username(self, username: str) -> User:
        user = self._db.get_user_by_username(username)
        return user

    def create_habit(self, habit: Habit):
        habit_id = self._db.create_habit(habit)
        return CreateHabitResponse(id=habit_id)

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
