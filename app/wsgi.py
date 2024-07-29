from app.controller import AppController

app = AppController()

def application(environ, start_response):
    return app.application(environ, start_response)