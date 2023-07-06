# Installing required dependencies

The following dependencies are required:
- `pipenv`: `python -m pip install pipenv`

```commandline
cd habit_backend
pipenv run uvicorn main:service
```

# Running tests

```commandline
cd habit_backend
pipenv run pytests
```