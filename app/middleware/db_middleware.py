from typing import Callable

from app.database import get_db
from app.repositories.match_repo import MatchRepo
from app.repositories.player_repo import PlayerRepo
from app.services.match_service import MatchService


def db_session_middleware(app: Callable) -> Callable:
    def middleware(environ, start_response):
        with get_db() as db_session:
            match_repo = MatchRepo(db_session)
            player_repo = PlayerRepo(db_session)
            match_service = MatchService(match_repo, player_repo)

            environ["match_service"] = match_service
            return app(environ, start_response)
    return middleware
