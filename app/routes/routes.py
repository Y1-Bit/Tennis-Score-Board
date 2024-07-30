from typing import Callable
from app.decorators import Router
from jinja2 import Environment

router = Router()

@router.get("/")
def index(start_response: Callable, template_env: Environment) -> list[bytes]:
    template = template_env.get_template('index.html')
    response_body = template.render()
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body.encode('utf-8')]

@router.get("/hello")
def hello(start_response: Callable, template_env: Environment) -> list[bytes]:
    template = template_env.get_template('hello.html')
    response_body = template.render()
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body.encode('utf-8')]

@router.post("/submit")
def submit(start_response: Callable, template_env: Environment) -> list[bytes]:
    template = template_env.get_template('submit.html')
    response_body = template.render()
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body.encode('utf-8')]
