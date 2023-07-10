import sqlite3


def drop_user_account_table(cur: sqlite3.Cursor):
    cur.execute("DROP TABLE IF EXISTS user_account")


def drop_habit_table(cur: sqlite3.Cursor):
    cur.execute("DROP TABLE IF EXISTS habit")


def drop_habit_event_table(cur: sqlite3.Cursor):
    cur.execute("DROP TABLE IF EXISTS habit_event")


def create_user_account_table(cur: sqlite3.Cursor):
    cur.execute("""    
        CREATE TABLE user_account (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(16) UNIQUE NOT NULL,
            email TEXT
            );
            """)


def create_habit_table(cur: sqlite3.Cursor):
    cur.execute("""
        CREATE TABLE habit (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP NOT NULL,
            user_id INT,
            task VARCHAR(80) NOT NULL,
            description TEXT,
    
            FOREIGN KEY (user_id) REFERENCES user_account(id)
        );"""
                )


def create_habit_event_table(cur: sqlite3.Cursor):
    cur.execute("""
        CREATE TABLE habit_event (
            id SERIAL PRIMARY KEY,
            user_id INT,
            habit_id INT,
            completed_at DATE NOT NULL,
    
            FOREIGN KEY (user_id) REFERENCES user_account(id),
            FOREIGN KEY (habit_id) REFERENCES habit(id)
        );"""
                )


def drop_tables(cur: sqlite3.Cursor):
    drop_user_account_table(cur)
    drop_habit_table(cur)
    drop_habit_event_table(cur)


def create_tables(cur: sqlite3.Cursor):
    create_user_account_table(cur)
    create_habit_table(cur)
    create_habit_event_table(cur)
