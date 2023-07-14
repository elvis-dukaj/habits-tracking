from sqlmodel import Session, select

from app.schemas.user import UserCreate, UserRead, User
from app.schemas.habit import HabitCreate, HabitRead, Habit
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

    def get_user_by_username(self, username: str):
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            result = session.exec(statement)
            user = result.first()

            if user is None:
                raise UserNotFoundError()

            return user

    def create_habit(self, habit: HabitCreate):
        with Session(self.engine) as session:
            created_habit = Habit.from_orm(habit)
            session.add(created_habit)
            session.commit()
            session.refresh(created_habit)
            return created_habit

    def delete_habit(self, habit_id):
        with Session(self.engine) as session:
            habit_to_delete = self.get_user_by_id(habit_id)
            session.delete(habit_to_delete)
            session.commit()

    def get_habit_by_id(self, habit_id):
        with Session(self.engine) as session:
            habit = session.get(Habit, habit_id)

            if habit is None:
                raise UserNotFoundError()

            return habit

    def get_habits(self, offset: int, limit: int):
        with Session(self.engine) as session:
            statement = select(Habit).offset(offset).limit(limit)
            result = session.exec(statement)
            return result.all()

    def get_habits_by_user_id(self, user_id: int, offset: int, limit: int):
        with Session(self.engine) as session:
            statement = select(Habit).where(Habit.user_id == user_id).offset(offset).limit(limit)
            result = session.exec(statement)
            return result.all()

    def get_habits_by_periodicity(self, periodicity: int, offset: int, limit: int):
        with Session(self.engine) as session:
            statement = select(Habit).where(Habit.periodicity == periodicity).offset(offset).limit(limit)
            result = session.exec(statement)
            return result.all()

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
