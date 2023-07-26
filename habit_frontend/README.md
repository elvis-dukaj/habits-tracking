# Setting up the CLI

The CLI requires a virtual environment to run:

For Posix-like system:

```commandline
python -m venv .venv
. .venv/bin/activate
pip install .
```

# Running the CLI

Now from inside the virtual environment it's possible to call the `htr` (HabitTRacker) terminal.

```commandline
htr --help
Usage: htr [OPTIONS] COMMAND [ARGS]...

Options:
  --endpoint TEXT  server endpoint
  --help           Show this message and exit.

Commands:
  habit
  statistic
  user
```

# User

```commandline
htr user --help
Usage: htr user [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create
  delete
  login
```

## Create a new user

```commandline
htr user create --help
Usage: htr user create [OPTIONS]

Options:
  --username TEXT  Username
  --help           Show this message and exit.
```

---
**NOTE**

If not specified the option `--username`, it will be prompted! This is
true for almost all the options

---

### Example:

```commandline
htr user create
Username: test_username
User 'test_username' created with user-id 4
```

This command return the user id. This command will be used for all the following
commands, but it's annoying to repeat all the time. We can avoid this by
adding a new environment variable called `HABIT_TRACKER_USER_ID`. For Unix-like
this can be done the following:

```commandline
export HABIT_TRACKER_USER_ID=1
```

## Delete an existing user

```commandline
htr user delete --help
Usage: htr user delete [OPTIONS]

Options:
  --user-id TEXT  Username
  --help          Show this message and exit.
```

### Example:

```commandline
htr user delete
User id: 4
User '4' deleted
```

## Login a User

```commandline
htr user login --help
Usage: htr user login [OPTIONS]

Options:
  --username TEXT  user to login
  --help           Show this message and exit.
```

### Example

```commandline
htr user login
Username: test_user
User 'test_user' logged in with user-id 4
```

## Habits

```commandline
htr habit --help
Usage: htr habit [OPTIONS] COMMAND [ARGS]...

Options:
  --user-id INTEGER  user  [required]
  --help             Show this message and exit.

Commands:
  complete
  create
  delete
  history
  list
  statistic
```

---
**NOTE**

We are assuming that the environment variable `HABIT_TRACKER_USER_ID`
is defined otherwise it's necessary add the option `--user-id` to the `habit`
command like following:

```commandline
htr habit --user-id ...
```

---

## Create a Habit

```commandline
htr habit create --help
Usage: htr habit create [OPTIONS]

Options:
  --task TEXT            short description of the task
  --periodicity INTEGER  periodicity in days
  --help                 Show this message and exit.
```

---
Example:

```commandline
htr habit create
Task: Yoga every morning
Periodicity: 1
Habit 'Yoga every morning' created with id 11
```

---

## Delete a Habit

```commandline
htr habit delete --help
Usage: htr habit delete [OPTIONS]

Options:
  --habit-id INTEGER  habit id to remove  [required]
  --help              Show this message and exit.
```

### Example

```commandline
htr habit delete
Habit id: 13
Habit '13' deleted
```

## Mark a Habit as completed

```commandline
htr habit complete --help
Usage: htr habit complete [OPTIONS]

Options:
  --habit-id INTEGER           habit id to mark as completed  [required]
  --completed-date [%Y-%m-%d]  habit to mark as completed  [required]
  --help                       Show this message and exit.
```

### Example

```commandline
htr habit complete
Habit id: 12
Completed date: 2023-08-17
Habit 'test' completed
```

## List habits

```commandline
htr habit list [OPTIONS]

Options:
  --with-periodicity INTEGER  filter by periodicity
  --help
```

### Example - list all habits

```commandline
htr habit list
+----+-----------+------------+---------------------------+---------------+
|    |   user_id |   habit_id | task                      |   periodicity |
|----+-----------+------------+---------------------------+---------------|
|  0 |         1 |          1 | stretch the nack          |             1 |
|  1 |         1 |          2 | stretch the back          |             1 |
|  2 |         1 |          3 | learn German              |             1 |
|  3 |         1 |          5 | call Oma                  |             7 |
|  4 |         1 |          6 | reading a book            |             1 |
|  5 |         1 |          7 | doing yoga in the morning |             1 |
|  6 |         1 |          8 | walk 2km                  |             2 |
|  7 |         1 |          9 | clean the flat            |            10 |
|  8 |         1 |         10 | study german              |             5 |
|  9 |         1 |         11 | Yoga every morning        |             1 |
+----+-----------+------------+---------------------------+---------------+
```

### Example - list all habits with a specific periodicity

```commandline
htr habit list --with-periodicity 1
+----+-----------+------------+---------------------------+---------------+
|    |   user_id |   habit_id | task                      |   periodicity |
|----+-----------+------------+---------------------------+---------------|
|  0 |         1 |          1 | stretch the nack          |             1 |
|  1 |         1 |          2 | stretch the back          |             1 |
|  2 |         1 |          3 | learn German              |             1 |
|  3 |         1 |          6 | reading a book            |             1 |
|  4 |         1 |          7 | doing yoga in the morning |             1 |
|  5 |         1 |         11 | Yoga every morning        |             1 |
+----+-----------+------------+---------------------------+---------------+
```

## View habit statistics

```commandline
htr habit statistic --help
Usage: htr habit statistic [OPTIONS]

Options:
  --habit-id INTEGER  habit to view  [required]
  --help              Show this message and exit
```

### Example

```commandline
htr habit statistic
Habit id: 7
+-----------+--------+----------+---------+-----------------+--------------------+----------+
|   Longest |   Last |   Median |    Mean |   Total Streaks |   Expected Streaks |    Score |
|-----------+--------+----------+---------+-----------------+--------------------+----------|
|         4 |      4 |        2 | 2.33333 |               7 |                 18 | 0.388889 |
+-----------+--------+----------+---------+-----------------+--------------------+----------+
```

## View Habit events history

```commandline
htr habit history --help
Usage: htr habit history [OPTIONS]

Options:
  --habit-id INTEGER  habit to view  [required]
  --help              Show this message and exit.
```

### Example

```commandline
htr habit history
Habit id: 7
+---------------------+---------------------+----------+
| Start Date          | End Date            |   Streak |
|---------------------+---------------------+----------|
| 2023-07-25 00:00:00 | 2023-07-27 00:00:00 |        2 |
| 2023-08-01 00:00:00 | 2023-08-02 00:00:00 |        1 |
| 2023-08-10 00:00:00 | 2023-08-12 00:00:00 |        4 |
+---------------------+---------------------+----------+
```

## Statistic

```commandline
htr statistic
Usage: htr statistic [OPTIONS] COMMAND [ARGS]...

Options:
  --user-id INTEGER  filter by habit id
  --help             Show this message and exit.

Commands:
  view
```

### View statistic

```commandline
htr statistic view --help
Usage: htr statistic view [OPTIONS]

Options:
  --order-by [habit|current|longest|mean|periodicity|score]
  --ascending
  --help                          Show this message and exit.
```

### Example -- View statistic, order ascending by score

```commandline
htr statistic view --order-by score --ascending
+------------+---------------------------+---------------+---------------+------------------+------------------+--------------------+----------+
|   Habit ID | Task                      |   Periodicity |   Last Streak |   Longest Streak |   Average Streak |   Expected Streaks |    Score |
|------------+---------------------------+---------------+---------------+------------------+------------------+--------------------+----------|
|          1 | stretch the nack          |             1 |             3 |                3 |          3       |                  3 | 1        |
|          2 | stretch the back          |             1 |             2 |                2 |          2       |                  2 | 1        |
|          3 | learn German              |             1 |             4 |                4 |          4       |                  4 | 1        |
|          5 | call Oma                  |             7 |             4 |                4 |          4       |                  2 | 1        |
|          6 | reading a book            |             1 |             1 |                1 |          1       |                  1 | 1        |
|          9 | clean the flat            |            10 |             2 |                3 |          2.6     |                  7 | 1        |
|          7 | doing yoga in the morning |             1 |             4 |                4 |          2.33333 |                 18 | 0.388889 |
|          8 | walk 2km                  |             2 |             0 |                0 |          0       |                  0 | 0        |
|         10 | study german              |             5 |             0 |                0 |          0       |                  0 | 0        |
|         11 | Yoga every morning        |             1 |             0 |                0 |          0       |                  0 | 0        |
+------------+---------------------------+---------------+---------------+------------------+------------------+--------------------+----------+
```