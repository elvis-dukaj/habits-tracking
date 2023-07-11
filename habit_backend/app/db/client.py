import datetime

import sqlite3

from app.schemas.user import User
from app.schemas.habit import Habit
from app.schemas.habit_event import HabitEvent
from app.exception import UserNotFoundError, HabitNotFoundError


class DatabaseClient:
    def __init__(self, host: str):
        self._connection: sqlite3.Connection = sqlite3.connect(host, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()

    def add_user(self, user: User) -> User:
        sql_command = "INSERT INTO user_account(username, email) VALUES(?, ?)"
        sql_args: tuple[str, str] = (user.username, user.email)

        self._cursor.execute(sql_command, sql_args)
        self._connection.commit()
        created_user_id = self._cursor.lastrowid

        return self.get_user_by_id(created_user_id)

    def delete_user(self, user_id):
        sql_command = "DELETE FROM user_account WHERE user_id = ?"
        sql_args: tuple[str] = (user_id,)

        self._cursor.execute(sql_command, sql_args)
        self._connection.commit()

    def get_user_by_id(self, user_id: int) -> User:
        sql_command = """
        SELECT * FROM user_account
        WHERE user_id = ?
        """
        sql_args = (user_id,)

        self._cursor.execute(sql_command, sql_args)
        row = self._cursor.fetchone()

        if row is None:
            raise UserNotFoundError()

        user = User(**row)
        return user

    def get_user_by_username(self, username: str) -> User:
        sql_command = """
        SELECT * FROM user_account
        WHERE username = ?
        """
        sql_args = (username,)
        self._cursor.execute(sql_command, sql_args)

        row = self._cursor.fetchone()

        if row is None:
            raise UserNotFoundError()

        user = User(**row)
        return user

    def create_habit(self, habit: Habit) -> Habit:
        # self._current_habit_id += 1
        # self._habits_db[self._current_habit_id] = dict(habit)
        # habit_raw = self._habits_db[self._current_habit_id]
        # habit_raw["habit_id"] = self._current_habit_id
        # habit_raw["created_at"] = datetime.date.today()
        # full_habit = Habit(**habit_raw)
        # return full_habit
        pass

    def delete_habit(self, habit_id: int):
        pass
        # if id not in self._habits_db:
        #     raise HabitNotFoundError
        #
        # del self._habits_db[habit_id]

    def get_habit_by_id(self, habit_id: int) -> Habit:
        pass
        # if habit_id not in self._habits_db:
        #     raise HabitNotFoundError()
        #
        # habit_data = self._habits_db[habit_id]
        # habit = Habit(**habit_data)
        # return habit

    def get_all_habits(self) -> list[Habit]:
        pass
        # habits: list[Habit] = []
        # for habit_id in self._habits_db:
        #     habit_raw = self._habits_db[habit_id]
        #     habit = Habit(**habit_raw)
        #     habits.append(habit)
        #
        # return habits

    def get_habits_by_user_id(self, user_id: int) -> list[Habit]:
        pass
        # result = []
        # habit_values = list(self._habits_db.values())
        # for habit_json in habit_values:
        #     habit = Habit(**habit_json)
        #     if habit.user_id == user_id:
        #         result.append(habit)
        #
        # return result

    def add_habit_event(self, user_id: int, habit_id: int) -> HabitEvent:
        pass
        # raw_event = self._habit_event_db[self._current_habit_event_id] = {
        #     "event_id": self._current_habit_event_id,
        #     "completed_at": datetime.date.today(),
        #     "user_id": user_id,
        #     "habit_id": habit_id
        # }
        # self._current_habit_event_id += 1
        #
        # return HabitEvent(**raw_event)
