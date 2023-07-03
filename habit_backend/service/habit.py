from schemas.habits import (
    User,
    CreateUserResponse,
    Habit
)


class HabitsTrackingService:
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
        self._current_id = len(self._user_db)

        self._habits_db = {
            1: {
                "task": "stretch the legs",
                "frequency": 1
            },
            2: {
                "task": "boulder",
                "periodicity": 3
            },
            3: {
                "task": "study",
                "frequency": 2
            },
            4: {
                "task": "call nonna",
                "frequency": 14
            },
            5: {
                "task": "massage the neck",
                "frequency": 7
            },
        }
        self._habit_current_id = len(self._habits_db)

    def create_user(self, user: User) -> CreateUserResponse:
        self._current_id += 1
        self._user_db[self._current_id] = dict(user)
        return CreateUserResponse(user_id=self._current_id)

    def delete_user(self, user_id: int) -> None:
        del self._user_db[user_id]

    def get_user_info_by_id(self, user_id: int) -> User:
        user = self._user_db[user_id]
        reply = User(**user)
        return reply

    def get_user_info_by_username(self, username: str) -> User:
        for user in self._user_db:
            print(user)
            current_user = self._user_db[user]
            if current_user["username"] == username:
                return User(**current_user)
