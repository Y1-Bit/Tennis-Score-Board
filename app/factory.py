from app.controller import AppController
from app.routes import router
from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_app() -> AppController:
    template_env = Environment(
        loader=FileSystemLoader("app/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    return AppController(router, template_env)
