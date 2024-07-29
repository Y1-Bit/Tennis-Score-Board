import logging
from urllib.parse import parse_qs
from typing import Callable, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from wsgiref.handlers import SimpleHandler

from app.decorators import Router

env = Environment(
    loader=FileSystemLoader('app/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class RequestHandler:
    def __init__(self, environ, start_response, router: Router) -> None:
        self.environ = environ
        self.start_response = start_response
        self.router = router

    def handle_request(self) -> list[bytes] | None:
        try:
            method = self.environ['REQUEST_METHOD']
            path = self.environ['PATH_INFO']
            query_string = self.environ.get('QUERY_STRING', '')
            query = parse_qs(query_string)

            handler, path_params = self.router.find_handler(method, path)
            if handler:
                if method == 'POST':
                    return self.handle_with_body(handler, path_params)
                elif method == 'GET':
                    return self.handle_get(handler, path_params, query)
            else:
                return self.handle_not_found()
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            return self.handle_error()

    def handle_error(self) -> list[bytes]:
        self.start_response('500 Internal Server Error', [('Content-Type', 'text/html')])
        return [b'<h1>Internal Server Error</h1>']

    def handle_not_found(self) -> list[bytes]:
        self.start_response('404 Not Found', [('Content-Type', 'text/html')])
        return [b'<h1>Not Found</h1>']

    def handle_with_body(self, handler: Callable, path_params: Optional[str] = None) -> list[bytes]:
        try:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            content_length = 0

        post_data = self.environ['wsgi.input'].read(content_length)
        form_data = parse_qs(post_data.decode('utf-8'))
        response = handler(form_data)
        self.start_response(f"{response['status_code']} OK", [('Content-Type', 'text/html')])
        return [response['body'].encode('utf-8')]

    def handle_get(self, handler: Callable, path_params: Optional[str], query: dict) -> list[bytes]:
        response = handler(query)
        self.start_response(f"{response['status_code']} OK", [('Content-Type', 'text/html')])
        return [response['body'].encode('utf-8')]