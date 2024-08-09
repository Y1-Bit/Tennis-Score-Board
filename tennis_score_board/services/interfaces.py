from typing import Protocol

from tennis_score_board.models.match import Match
from tennis_score_board.models.player import Player


class MatchRepoInterface(Protocol):
    def add(self, match: Match) -> Match: ...
    def get_all(self) -> list[Match]: ...
    def get_by_id(self, match_id: int) -> Match: ...


class PlayerRepoInterface(Protocol):
    def get_or_create(self, player_name: str) -> Player: ...
