from typing import Callable

class AppController:
    def __init__(self) -> None:
        self.routes = {
            "/": self.index,
            "/hello": self.hello
        }

    def index(self, start_response: Callable):
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Welcome to the Index Page"]
    
    def hello(self, start_response: Callable):
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Hello, World!"]

    def not_found(self, start_response: Callable):  
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"404 Not Found"]
    
    def application(self, environ: dict, start_response: Callable):
        path = environ.get('PATH_INFO', '/')
        route = self.routes.get(path, self.not_found)
        return route(start_response)