from schemas.user import User
from schemas.habit import Habit
from exception import UserNotFoundError, HabitNotFoundError


class DatabaseClient():
    def __init__(self):
        self._user_db = {
            1: {
                "username": "elvis.dukaj",
                "email": "elvis.dukaj@gmail.com"
            },
            2: {
                "username": "stefanie.zoechmann",
                "email": "stefanie.zoechmann@gmail.com"
            }
        }
        self._current_user_id = len(self._user_db)

        self._habits_db = {
            1: {
                "user_id": 1,
                "task": "stretch the legs",
                "description": "",
                "periodicity": 1
            },
            2: {
                "user_id": 1,
                "task": "boulder",
                "description": "",
                "periodicity": 3
            },
            3: {
                "user_id": 2,
                "task": "study",
                "description": "",
                "periodicity": 2
            },
            4: {
                "user_id": 2,
                "task": "call nonna",
                "description": "",
                "periodicity": 14
            },
            5: {
                "user_id": 1,
                "task": "massage the neck",
                "description": "",
                "periodicity": 7
            },
        }
        self._current_habit_id = len(self._habits_db)

    def add_user(self, user: User) -> int:
        self._current_user_id += 1
        self._user_db[self._current_user_id] = dict(user)
        return self._current_user_id

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
        for user in self._user_db:
            print(user)
            current_user = self._user_db[user]
            if current_user["username"] == username:
                return User(**current_user)

        raise UserNotFoundError()

    def create_habit(self, habit: Habit):
        self._current_habit_id += 1
        self._habits_db[self._current_habit_id] = dict(habit)
        return self._current_habit_id

    def delete_habit(self, id: int):
        if id not in self._habits_db:
            raise HabitNotFoundError

        del self._habits_db[id]

    def get_habit_by_id(self, id: int) -> Habit:
        if id not in self._habits_db:
            raise HabitNotFoundError()

        habit = self._habits_db[id]
        reply = Habit(**habit)
        return reply

    def get_all_habits(self) -> list[Habit]:
        habit_values = list(self._habits_db.values())
        return [*habit_values]

    def get_habits_by_user_id(self, user_id: int) -> list[Habit]:
        result = []
        habit_values = list(self._habits_db.values())
        for habit_json in habit_values:
            habit = Habit(**habit_json)
            if habit.user_id == user_id:
                result.append(habit)

        return result

