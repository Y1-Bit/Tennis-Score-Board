from app.models.match import Match
from app.repositories.interfaces import MatchRepoInterface, PlayerRepoInterface


class MatchService:
    def __init__(
        self, match_repo: MatchRepoInterface, player_repo: PlayerRepoInterface
    ):
        self.match_repo = match_repo
        self.player_repo = player_repo

    def create_match(self, player1_name: str, player2_name: str) -> Match:
        player1 = self.player_repo.get_or_create(player1_name)
        player2 = self.player_repo.get_or_create(player2_name)
        new_match = Match(player1_id=player1.id, player2_id=player2.id)
        return self.match_repo.add(new_match)

    def list_matches(self) -> list[Match]:
        return self.match_repo.get_all()

    def get_match(self, match_id: int) -> Match:
        return self.match_repo.get_by_id(match_id)
