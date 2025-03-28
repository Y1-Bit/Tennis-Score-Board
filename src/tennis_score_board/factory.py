import logging
import os
from typing import Callable

from jinja2 import Environment, FileSystemLoader, select_autoescape

from mini_framework import RequestHandler, static_files_middleware
from tennis_score_board.adapters.infrastructure.database.database import init_database
from tennis_score_board.adapters.presentation.middleware.db_middleware import \
    db_session_middleware
from tennis_score_board.adapters.presentation.routes import router
from tennis_score_board.config import Config, load_config


def create_app(config_path: str | None = None) -> Callable:
    config = load_config(config_path)
    database = init_database(config)  

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(base_dir, "tennis_score_board", "adapters/presentation/static")

    template_env = Environment(
        loader=FileSystemLoader(
            os.path.join(base_dir, "tennis_score_board", "adapters/presentation/templates")
        ),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template_env.globals["url_for_static"] = lambda filename: f"/static/{filename}"

    logger = logging.getLogger("tennis_score_board")
    request_handler = RequestHandler(router, template_env, logger)
    app_with_middleware = db_session_middleware(request_handler.application, database)
    app_with_static = static_files_middleware(app_with_middleware, static_dir)

    return app_with_static
