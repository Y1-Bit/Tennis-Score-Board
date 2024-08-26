from typing import Protocol

from tennis_score_board.domain.match import Match, MatchList
from tennis_score_board.domain.player import Player


class MatchRepoInterface(Protocol):
    def add(self, match: Match, player1: Player, player2: Player) -> Match: ...
    def update(self, match: Match) -> Match: ...
    def get_all(self) -> MatchList: ...
    def get_by_uuid(self, uuid: str) -> Match: ...
    def get_matches(
        self, page: int, filter_by_player_name: str | None = None, per_page: int = 10
    ) -> tuple[list[Match], int]: ...


class PlayerRepoInterface(Protocol):
    def get_or_create(self, player_name: str) -> Player: ...
