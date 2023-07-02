The Habit App will be composed by two components. A web service and a front-end.

The service will use internally a PostgreSQL for storing persistent data. I am planning to use 3 tables:
 - user: will store information about the user (id, created_at, username, email)
 - habit: it will store information about habits (id, user_id, created_at, task, periodicity)
 - habit_event: it will store the timestamp of a given completed habit (id, user_id, habit_id, completed)

The service will provide a REST API for managing users, habits, and habit events and for getting analytics,
i.e. get all the streaks, get the longest streak for a specific habit.

The front-end will be a CLI that essentially calls he habit_service.

If I have enough time I could create a web front end providing the same functionalities.

I am aware that I won't have extra credit for adding extra features like the user management or providing a GUI but I
would like to have the following project as much as possible to be production-ready




## POST/PUT:

- create new user 
  - /user/user_id <username><password><email>
  - params: username password email
  - returns user_id
- create a new habit 
  - /habit
  - params: user_id, periodicity, name, description
  - return habit_id
- complete a habit:
  - /habit_log
  - parameters: habit_id

## DELETE

- delete user:
  - /user/user_id
- delete habit
  - /habit/habit_id
- delete habit log
  - /habit_log

## GET:

- get all users:
  - /user
- get all habits
  - /habit
- get all habits for a user
  - /habit/user_id
- get all habit_log
  - /habit_log
- get all habit_log for user and habit
  - /habit_log/user_id/habit_id

### Analytics

- get all habit by frequency
  - /habit/habit_id/frequency
  

