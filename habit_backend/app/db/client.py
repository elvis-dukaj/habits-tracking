from sqlmodel import Session, select

from app.schemas.user import UserCreate, UserRead, User
from app.exception import UserNotFoundError


class DatabaseClient:
    def __init__(self, engine):
        self.engine = engine

    def add_user(self, user: UserCreate) -> UserRead:
        created_user = user
        with Session(self.engine) as session:
            db_hero = User.from_orm(user)
            session.add(db_hero)
            session.commit()
            session.refresh(db_hero)
            return db_hero

    def delete_user(self, user_id):
        with Session(self.engine) as session:
            user_to_delete = self.get_user_by_id(user_id)
            session.delete(user_to_delete)
            session.commit()

    def get_user_by_id(self, user_id: int) -> UserRead:
        with Session(self.engine) as session:
            user = session.get(User, user_id)

            if user is None:
                raise UserNotFoundError()

            return user

    def get_user_by_username(self, username: str) -> UserRead:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            result = session.exec(statement)
            user = result.first()

            if user is None:
                raise UserNotFoundError()

            return user

    # def create_habit(self, habit: Habit) -> Habit:
    #     # self._current_habit_id += 1
    #     # self._habits_db[self._current_habit_id] = dict(habit)
    #     # habit_raw = self._habits_db[self._current_habit_id]
    #     # habit_raw["habit_id"] = self._current_habit_id
    #     # habit_raw["created_at"] = datetime.date.today()
    #     # full_habit = Habit(**habit_raw)
    #     # return full_habit
    #     pass
    #
    # def delete_habit(self, habit_id: int):
    #     pass
    #     # if id not in self._habits_db:
    #     #     raise HabitNotFoundError
    #     #
    #     # del self._habits_db[habit_id]
    #
    # def get_habit_by_id(self, habit_id: int) -> Habit:
    #     pass
    #     # if habit_id not in self._habits_db:
    #     #     raise HabitNotFoundError()
    #     #
    #     # habit_data = self._habits_db[habit_id]
    #     # habit = Habit(**habit_data)
    #     # return habit
    #
    # def get_all_habits(self) -> list[Habit]:
    #     pass
    #     # habits: list[Habit] = []
    #     # for habit_id in self._habits_db:
    #     #     habit_raw = self._habits_db[habit_id]
    #     #     habit = Habit(**habit_raw)
    #     #     habits.append(habit)
    #     #
    #     # return habits
    #
    # def get_habits_by_user_id(self, user_id: int) -> list[Habit]:
    #     pass
    #     # result = []
    #     # habit_values = list(self._habits_db.values())
    #     # for habit_json in habit_values:
    #     #     habit = Habit(**habit_json)
    #     #     if habit.user_id == user_id:
    #     #         result.append(habit)
    #     #
    #     # return result
    #
    # def add_habit_event(self, user_id: int, habit_id: int) -> HabitEvent:
    #     pass
    #     # raw_event = self._habit_event_db[self._current_habit_event_id] = {
    #     #     "event_id": self._current_habit_event_id,
    #     #     "completed_at": datetime.date.today(),
    #     #     "user_id": user_id,
    #     #     "habit_id": habit_id
    #     # }
    #     # self._current_habit_event_id += 1
    #     #
    #     # return HabitEvent(**raw_event)
