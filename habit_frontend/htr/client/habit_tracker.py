import requests
import datetime
from pydantic import BaseModel


class Habit(BaseModel):
    user_id: int
    habit_id: int
    task: str
    periodicity: int


class HabitTrackerClient:
    def __init__(self, endpoint: str):
        self.endpoint: str = endpoint
        self.user_prefix: str = f"{self.endpoint}/user"
        self.habit_prefix: str = f"{self.endpoint}/habit"
        self.habit_event_prefix: str = f"{self.endpoint}/habit_event"
        self._current_user_id: int = 0

    def set_current_user_id(self, user_id: int):
        self._current_user_id = user_id

    def add_user(self, username: str) -> int:
        json_body = {
            "username": username
        }

        response = requests.post(url=self.user_prefix, json=json_body)

        if response.status_code != 201:
            raise Exception("user not created")

        user_id = response.json()["user_id"]
        return user_id

    def delete_user(self, user_id: int):
        url = f"{self.user_prefix}/{user_id}"
        response = requests.delete(url)

        if response.status_code != 200:
            raise Exception("user not deleted")

    def login(self, username: str) -> int:
        url = f"{self.user_prefix}/username/{username}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"user {username} not found")

        user_id = response.json()["user_id"]

        return user_id

    def create_habit(self, task: str, periodicity: int):
        json_body = {
            "user_id": self._current_user_id,
            "task": task,
            "periodicity": periodicity
        }

        response = requests.post(url=self.habit_prefix, json=json_body)

        if response.status_code != 201:
            raise Exception("habit not created")

        habit_id = response.json()["habit_id"]
        return habit_id

    def delete_habit(self, habit_id: int):
        url = f"{self.habit_prefix}/{habit_id}"
        response = requests.delete(url)

        if response.status_code != 200:
            raise Exception("habit not deleted")

    def list_habits_by_periodicity(self, periodicity: int) -> list[Habit]:
        url = f"{self.habit_prefix}/?user_id={self._current_user_id}&periodicity={periodicity}&offset=0&limit=100"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("an error")

        json_reply = response.json()

        habits: list[Habit] = []

        for habit_json in json_reply:
            habit: Habit = Habit(**habit_json)
            habits.append(habit)

        return habits

    def mark_habit_completed(self, habit_id: int, completed_at: datetime.date):
        json_body = {
            "user_id": self._current_user_id,
            "habit_id": habit_id,
            "completed_at": str(completed_at)
        }
        print(f"I want to send ti {self.habit_event_prefix} this: {json_body}")
        response = requests.post(url=self.habit_event_prefix, json=json_body)

        if response.status_code != 201:
            raise Exception("an error")

        json_reply = response.json()

        habits: list[Habit] = []
