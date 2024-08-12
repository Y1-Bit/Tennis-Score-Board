import logging
from typing import Callable
from urllib.parse import parse_qs

from jinja2 import Environment

from tennis_score_board.core.router import Router


class RequestHandler:
    def __init__(
        self, router: Router, template_env: Environment, logger: logging.Logger
    ) -> None:
        self.router = router
        self.template_env = template_env
        self.logger = logger

    def not_found(self, start_response: Callable):
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"404 Not Found"]

    def server_error(self, start_response: Callable):
        start_response(
            "500 Internal Server Error", [("Content-Type", "text/plain; charset=utf-8")]
        )
        error_message = f"Internal Server Error"
        return [error_message.encode("utf-8")]

    def application(self, environ: dict, start_response: Callable):
        try:
            method = environ.get("REQUEST_METHOD", "GET")
            path = environ.get("PATH_INFO", "/")
            handler = self.router.find_handler(method, path)

            if handler:
                if method == "POST":
                    content_length = int(environ.get("CONTENT_LENGTH", 0))
                    body = environ["wsgi.input"].read(content_length).decode()
                    form_data = parse_qs(body)
                    return handler(
                        start_response, self.template_env, environ, form_data
                    )
                else:
                    return handler(start_response, self.template_env)
            else:
                return self.not_found(start_response)
        except Exception as e:
            self.logger.exception(f"Error handling request: {e}")
            return self.server_error(start_response)
