from typing import Callable
from urllib.parse import parse_qs

from jinja2 import Environment

from app.decorators import Router


class AppController:
    def __init__(self, router: Router, template_env: Environment) -> None:
        self.router = router
        self.template_env = template_env

    def not_found(self, start_response: Callable):
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"404 Not Found"]

    def application(self, environ: dict, start_response: Callable):
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        handler = self.router.find_handler(method, path)

        if handler:
            if method == "POST":
                content_length = int(environ.get("CONTENT_LENGTH", 0))
                body = environ["wsgi.input"].read(content_length).decode()
                form_data = parse_qs(body)
                return handler(start_response, self.template_env, environ, form_data)
            else:
                return handler(start_response, self.template_env)
        else:
            return self.not_found(start_response)
