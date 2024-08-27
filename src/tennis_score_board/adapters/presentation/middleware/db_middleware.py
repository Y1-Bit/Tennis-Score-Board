from typing import Callable

from tennis_score_board.adapters.infrastructure.database.database import Database
from tennis_score_board.adapters.infrastructure.database.transaction_manager import (
    TransactionManager,
)
from tennis_score_board.adapters.infrastructure.repositories.match_repo import MatchRepo
from tennis_score_board.adapters.infrastructure.repositories.player_repo import (
    PlayerRepo,
)
from tennis_score_board.application.services.match_service import MatchService


def db_session_middleware(app: Callable, database: Database) -> Callable:
    def middleware(environ, start_response):
        with database.get_db() as db_session:
            transaction_manager = TransactionManager(db_session)
            match_repo = MatchRepo(db_session)
            player_repo = PlayerRepo(db_session)
            match_service = MatchService(match_repo, player_repo, transaction_manager)

            environ["match_service"] = match_service
            return app(environ, start_response)

    return middleware
