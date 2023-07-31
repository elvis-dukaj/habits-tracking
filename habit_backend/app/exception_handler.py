from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.exception import UserNotFoundError, HabitNotFoundError


def add_exception_handler(service: FastAPI) -> None:
    @service.exception_handler(UserNotFoundError)
    def handle_user_not_found_exception(request: Request, exc: UserNotFoundError):
        return JSONResponse(status_code=404, content="User not found")

    @service.exception_handler(HabitNotFoundError)
    def handle_habit_not_found_exception(request: Request, exc: HabitNotFoundError):
        return JSONResponse(status_code=404, content="Habit not found")

    return None
