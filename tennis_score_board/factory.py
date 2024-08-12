from typing import Callable

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tennis_score_board.core import RequestHandler
from tennis_score_board.middleware import db_session_middleware
from tennis_score_board.routes import router


def create_app() -> Callable:
    template_env = Environment(
        loader=FileSystemLoader("tennis_score_board/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    request_handler = RequestHandler(router, template_env)
    app_with_middleware = db_session_middleware(request_handler.application)
    return app_with_middleware
