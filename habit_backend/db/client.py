import datetime

from schemas.user import User
from schemas.habit import Habit
from schemas.habit_event import HabitEvent
from exception import UserNotFoundError, HabitNotFoundError


class DatabaseClient:
    def __init__(self):
        self._user_db = {
            1: {
                "username": "elvis.dukaj",
                "email": "elvis.dukaj@gmail.com",
                "created_at": datetime.date.today()
            },
            2: {
                "username": "stefanie.zoechmann",
                "email": "stefanie.zoechmann@gmail.com",
                "created_at": datetime.date.today()
            }
        }
        self._current_user_id = len(self._user_db)

        self._habits_db = {
            1: {
                "habit_id": 1,
                "created_at": datetime.date.today(),
                "user_id": 1,
                "task": "stretch the legs",
                "description": "",
                "periodicity": 1
            },
            2: {
                "habit_id": 2,
                "created_at": datetime.date.today(),
                "user_id": 1,
                "task": "boulder",
                "description": "",
                "periodicity": 3
            },
            3: {
                "habit_id": 3,
                "created_at": datetime.date.today(),
                "user_id": 2,
                "task": "study",
                "description": "",
                "periodicity": 2
            },
            4: {
                "habit_id": 4,
                "created_at": datetime.date.today(),
                "user_id": 2,
                "task": "call nonna",
                "description": "",
                "periodicity": 14
            },
            5: {
                "habit_id": 5,
                "created_at": datetime.date.today(),
                "user_id": 1,
                "task": "massage the neck",
                "description": "",
                "periodicity": 7,
            },
        }
        self._current_habit_id = len(self._habits_db)

        self._habit_event_db = {
        }
        self._current_habit_event_id = 0

    def add_user(self, user: User) -> User:
        self._current_user_id += 1
        user_raw = self._user_db[self._current_user_id] = dict(user)
        user_raw["user_id"] = self._current_user_id
        user_raw["created_at"] = datetime.date.today()
        full_user = User(**user_raw)
        return full_user

    def delete_user(self, id):
        if id not in self._user_db:
            raise UserNotFoundError

        del self._user_db[id]

    def get_user_by_id(self, id: int) -> User:
        if id not in self._user_db:
            raise UserNotFoundError()

        user = self._user_db[id]
        reply = User(**user)
        return reply

    def get_user_by_username(self, username: str) -> User:
        for user_id in self._user_db:
            current_user = self._user_db[user_id]
            if current_user["username"] == username:
                return User(user_id=user_id, **current_user)

        raise UserNotFoundError()

    def create_habit(self, habit: Habit) -> Habit:
        self._current_habit_id += 1
        self._habits_db[self._current_habit_id] = dict(habit)
        habit_raw = self._habits_db[self._current_habit_id]
        habit_raw["habit_id"] = self._current_habit_id
        habit_raw["created_at"] = datetime.date.today()
        full_habit = Habit(**habit_raw)
        return full_habit

    def delete_habit(self, habit_id: int):
        if id not in self._habits_db:
            raise HabitNotFoundError

        del self._habits_db[habit_id]

    def get_habit_by_id(self, habit_id: int) -> Habit:
        if habit_id not in self._habits_db:
            raise HabitNotFoundError()

        habit_data = self._habits_db[habit_id]
        habit = Habit(**habit_data)
        return habit

    def get_all_habits(self) -> list[Habit]:
        habits: list[Habit] = []
        for habit_id in self._habits_db:
            habit_raw = self._habits_db[habit_id]
            habit = Habit(**habit_raw)
            habits.append(habit)

        return habits

    def get_habits_by_user_id(self, user_id: int) -> list[Habit]:
        result = []
        habit_values = list(self._habits_db.values())
        for habit_json in habit_values:
            habit = Habit(**habit_json)
            if habit.user_id == user_id:
                result.append(habit)

        return result

    def add_habit_event(self, user_id: int, habit_id: int) -> HabitEvent:
        raw_event = self._habit_event_db[self._current_habit_event_id] = {
            "event_id": self._current_habit_event_id,
            "completed_at": datetime.date.today(),
            "user_id": user_id,
            "habit_id": habit_id
        }
        self._current_habit_event_id += 1

        return HabitEvent(**raw_event)
