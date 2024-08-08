from typing import Callable

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.controller import AppController
from app.middleware import db_session_middleware
from app.routes import router


def create_app() -> Callable:
    template_env = Environment(
        loader=FileSystemLoader("app/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    app_controller = AppController(router, template_env)
    app_with_middleware = db_session_middleware(app_controller.application)
    return app_with_middleware
