from tennis_score_board.domain.match import Match
from tennis_score_board.application.interfaces import (
    MatchRepoInterface,
    PlayerRepoInterface,
)

from tennis_score_board.adapters.infrastructure.database import TransactionManager


class MatchService:
    def __init__(
        self,
        match_repo: MatchRepoInterface,
        player_repo: PlayerRepoInterface,
        transaction_manager: TransactionManager,
    ):
        self.match_repo = match_repo
        self.player_repo = player_repo
        self.transaction_manager = transaction_manager

    def create_match(self, player1_name: str, player2_name: str) -> Match:
        with self.transaction_manager.transaction():
            player1 = self.player_repo.get_or_create(player1_name)
            player2 = self.player_repo.get_or_create(player2_name)
            new_match = Match.create(player1.id, player2.id)
            return self.match_repo.add(new_match)
    
    def update_match_score(self, match_uuid: str, winning_player: str) -> Match:
        with self.transaction_manager.transaction():
            match = self.match_repo.get_by_uuid(match_uuid)
            match.add_point(winning_player)
            return self.match_repo.update(match)

    def get_match(self, match_uuid: str) -> Match:
        with self.transaction_manager.transaction():
            return self.match_repo.get_by_uuid(match_uuid)
        
    def get_matches(self, page: int, filter_by_player_name: str | None = None, per_page: int = 10) -> tuple[list[Match], int]:
        with self.transaction_manager.transaction():
            return self.match_repo.get_matches(page, filter_by_player_name, per_page)
    
