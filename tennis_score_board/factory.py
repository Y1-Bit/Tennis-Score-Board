from typing import Callable

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tennis_score_board.controller import AppController
from tennis_score_board.middleware import db_session_middleware
from tennis_score_board.routes import router


def create_app() -> Callable:
    template_env = Environment(
        loader=FileSystemLoader("app/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    app_controller = AppController(router, template_env)
    app_with_middleware = db_session_middleware(app_controller.application)
    return app_with_middleware
