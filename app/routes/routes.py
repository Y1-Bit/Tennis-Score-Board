from typing import Callable
from app.decorators import Router

router = Router()


@router.get("/")
def index(start_response: Callable) -> list[bytes]:
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Welcome to the Index Page"]


@router.get("/hello")
def hello(start_response: Callable) -> list[bytes]:
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Hello, World!"]


@router.post("/submit")
def submit(start_response: Callable) -> list[bytes]:
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Form submitted!"]
