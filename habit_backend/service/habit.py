from habit_backend.schemas.habits import User, UserResponse, Habit


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

    def create_user(self, user: User) -> int:
        self._current_id += 1
        self._db[self._current_id] = dict(user)
        return self._current_id

    def get_user_info(self, user_id: int) -> UserResponse:
        user = self._db[user_id]
        data = {
            "username": user["username"],
            "email": user["email"]
        }

        reply = UserResponse(**data)
        return reply

    def create_habit(self, user_id, habit: Habit):
        pass
