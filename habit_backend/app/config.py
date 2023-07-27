import os


class Config:
    db_host = os.environ.get("HABIT_DB_HOST", "sqlite:///htr.db")
