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

# REST API

The OpenAPI documentation is generated at url http://localhost:8000/docs#/ or
an alternative documentation can be founded at http://localhost:8000/redoc

---
**NOTE**

The server **must** be running to view the documentation

---