from tennis_score_board.database.transaction_manager import TransactionManager
from tennis_score_board.domain.match import Match, MatchList
from tennis_score_board.services.interfaces import (
    MatchRepoInterface,
    PlayerRepoInterface,
)


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

    def list_matches(self) -> MatchList:
        with self.transaction_manager.transaction():
            return self.match_repo.get_all()

    def get_match(self, match_id: int) -> Match:
        with self.transaction_manager.transaction():
            return self.match_repo.get_by_uuid(match_id)
