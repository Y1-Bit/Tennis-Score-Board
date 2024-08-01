from typing import Callable

from jinja2 import Environment
from sqlalchemy.orm import Session

from app.decorators import Router
from app.services.match_service import create_match

router = Router()


@router.get("/")
def index(start_response: Callable, template_env: Environment) -> list[bytes]:
    template = template_env.get_template("index.html")
    response_body = template.render()
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body.encode("utf-8")]


@router.post("/matches")
def create_new_match(start_response: Callable, template_env: Environment, db_session: Session, form_data: dict) -> list[bytes]:
    try:
        new_match = create_match(db_session, form_data)
        
        template = template_env.get_template("match.html")
        response_body = template.render(match=new_match)

        start_response("201 Created", [("Content-Type", "text/html; charset=utf-8")])
        return [response_body.encode("utf-8")]
    
    except ValueError as e:
        start_response("400 Bad Request", [("Content-Type", "text/plain; charset=utf-8")])
        return [str(e).encode("utf-8")]
    
    except Exception as e:
        start_response("500 Internal Server Error", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Internal Server Error"]