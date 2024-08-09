from typing import Protocol, List

from tennis_score_board.domain.match import Match
from tennis_score_board.domain.match import MatchList
from tennis_score_board.domain.player import Player


class MatchRepoInterface(Protocol):
    def add(self, match: Match) -> Match: ...
    def get_all(self) -> MatchList: ...
    def get_by_id(self, match_id: int) -> Match: ...


class PlayerRepoInterface(Protocol):
    def get_or_create(self, player_name: str) -> Player: ...
