from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from exception import UserNotFoundError


def add_exception_handler(service: FastAPI) -> None:
    @service.exception_handler(UserNotFoundError)
    def handle_user_not_found_exception(request: Request, exc: UserNotFoundError):
        return JSONResponse(status_code=404, content="User not found")

    return None
