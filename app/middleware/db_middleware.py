from typing import Callable

from app.database import get_db


def db_session_middleware(app: Callable) -> Callable:
    def middleware(environ, start_response):
        with get_db() as db:
            environ["db_session"] = db
            return app(environ, start_response)

    return middleware
