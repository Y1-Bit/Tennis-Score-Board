from typing import Callable

from jinja2 import Environment

from tennis_score_board.core.router import Router
from tennis_score_board.services.match_service import MatchService

router = Router()


@router.get("/")
def index(start_response: Callable, template_env: Environment) -> list[bytes]:
    template = template_env.get_template("index.html")
    response_body = template.render()
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body.encode("utf-8")]


@router.post("/matches")
def create_new_match(
    start_response: Callable, template_env: Environment, environ: dict, form_data: dict
) -> list[bytes]:
    match_service: MatchService = environ["match_service"]
    try:
        player1_name = form_data["player1"][0]
        player2_name = form_data["player2"][0]

        new_match = match_service.create_match(player1_name, player2_name)

        template = template_env.get_template("match.html")
        response_body = template.render(match=new_match)

        start_response("201 Created", [("Content-Type", "text/html; charset=utf-8")])
        return [response_body.encode("utf-8")]

    except KeyError as e:
        error_message = f"Missing required field: {str(e)}"
        start_response("400 Bad Request", [("Content-Type", "text/plain; charset=utf-8")])
        return [error_message.encode("utf-8")]

