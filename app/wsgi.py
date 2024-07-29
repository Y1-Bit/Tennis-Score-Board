from app.controller import AppController
from app.routes import router

app = AppController(router)


def application(environ, start_response):
    return app.application(environ, start_response)
