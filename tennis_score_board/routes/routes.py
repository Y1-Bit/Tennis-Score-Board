from typing import Callable

from jinja2 import Environment

from tennis_score_board.core.router import Router
from tennis_score_board.exceptions import MatchNotFoundError
from tennis_score_board.services.match_service import MatchService

router = Router()


@router.get("/")
def index(start_response: Callable, template_env: Environment, *args) -> list[bytes]:
    template = template_env.get_template("index.html")
    response_body = template.render()
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body.encode("utf-8")]


@router.get("/new-match")
def new_match_form(
    start_response: Callable, template_env: Environment, *args
) -> list[bytes]:
    template = template_env.get_template("new_match.html")
    response_body = template.render()
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [response_body.encode("utf-8")]


@router.post("/new-match")
def create_new_match(
    start_response: Callable,
    template_env: Environment,
    environ: dict,
    form_data: dict,
) -> list[bytes]:
    match_service: MatchService = environ["match_service"]
    try:
        player1_name = form_data["player1"][0]
        player2_name = form_data["player2"][0]
        new_match = match_service.create_match(player1_name, player2_name)

        start_response(
            "302 Found", [("Location", f"/match-score?uuid={new_match.uuid}")]
        )
        return []
    except KeyError as e:
        error_message = f"Missing required field: {str(e)}"
        start_response(
            "400 Bad Request", [("Content-Type", "text/plain; charset=utf-8")]
        )
        return [error_message.encode("utf-8")]


@router.get("/match-score")
def match_score(
    start_response: Callable,
    template_env: Environment,
    environ: dict,
    query_params: dict,
) -> list[bytes]:
    match_service: MatchService = environ["match_service"]
    try:
        match_uuid = query_params.get("uuid", [""])[0]
        match = match_service.get_match(match_uuid)
        template = template_env.get_template("match_score.html")
        response_body = template.render(match=match)
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [response_body.encode("utf-8")]
    except MatchNotFoundError:
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"404 Not Found"]


@router.post("/match-score")
def update_match_score(
    start_response: Callable, template_env: Environment, environ: dict, form_data: dict
) -> list[bytes]:
    match_service: MatchService = environ["match_service"]
    try:
        match_uuid = form_data["uuid"][0]
        winning_player = form_data["winning_player"][0]

        updated_match = match_service.update_match_score(match_uuid, winning_player)

        if updated_match.is_finished:
            template = template_env.get_template("match_finished.html")
            response_body = template.render(match=updated_match)
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [response_body.encode("utf-8")]
        else:
            start_response(
                "302 Found", [("Location", f"/match-score?uuid={updated_match.uuid}")]
            )
            return []
    except MatchNotFoundError:
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"404 Not Found"]
    except KeyError as e:
        error_message = f"Missing required field: {str(e)}"
        start_response(
            "400 Bad Request", [("Content-Type", "text/plain; charset=utf-8")]
        )
        return [error_message.encode("utf-8")]



@router.get("/matches")
def matches(
    start_response: Callable,
    template_env: Environment,
    environ: dict,
    query_params: dict
) -> list[bytes]:
    match_service: MatchService = environ["match_service"]
    try:
        page = int(query_params.get("page", ["1"])[0])
        filter_by_player_name = query_params.get("filter_by_player_name", [None])[0]
        per_page = 10  

        matches, total_pages = match_service.match_repo.get_matches(
            page=page,
            filter_by_player_name=filter_by_player_name,
            per_page=per_page
        )

        template = template_env.get_template("matches.html")
        response_body = template.render(
            matches=matches,
            page=page,
            total_pages=total_pages,
            query_params=query_params
        )

        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [response_body.encode("utf-8")]
    except KeyError as e:
        error_message = f"Missing required field: {str(e)}"
        start_response(
            "400 Bad Request", [("Content-Type", "text/plain; charset=utf-8")]
        )
        return [error_message.encode("utf-8")]
    