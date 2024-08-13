import json
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Match:
    id: Optional[int] = None
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    player1_id: int | None = None
    player2_id: int | None = None
    winner_id: Optional[int] = None
    score: dict = field(
        default_factory=lambda: {
            "player1": 0,
            "player2": 0,
            "set1": {"player1": 0, "player2": 0},
            "set2": {"player1": 0, "player2": 0},
            "set3": {"player1": 0, "player2": 0},
        }
    )

    @classmethod
    def create(cls, player1_id: int, player2_id: int) -> "Match":
        return cls(player1_id=player1_id, player2_id=player2_id)

    @property
    def is_finished(self) -> bool:
        return self.winner_id is not None

    def add_point(self, player: str):
        if self.winner_id is not None:
            raise ValueError("Match is already finished")

        current_set = self._get_current_set()
        self.score[player] += 1

        if self._is_game_won(player):
            self.score[current_set][player] += 1
            self._reset_game_score()

            if self._is_set_won(player, current_set):
                if self._is_match_won(player):
                    self.winner_id = (
                        self.player1_id if player == "player1" else self.player2_id
                    )
                else:
                    self._start_new_set()

    def _get_current_set(self) -> str:
        for set_name in ["set1", "set2", "set3"]:
            if (
                self.score[set_name]["player1"] < 6
                and self.score[set_name]["player2"] < 6
            ):
                return set_name
        raise ValueError("All sets are finished")

    def _is_game_won(self, player: str) -> bool:
        opponent = self._get_opponent(player)
        return (
            self.score[player] >= 4 and self.score[player] - self.score[opponent] >= 2
        )

    def _reset_game_score(self):
        self.score["player1"] = 0
        self.score["player2"] = 0

    def _is_set_won(self, player: str, current_set: str) -> bool:
        opponent = self._get_opponent(player)
        player_score = self.score[current_set][player]
        opponent_score = self.score[current_set][opponent]
        return (player_score == 6 and opponent_score <= 4) or (
            player_score == 7 and opponent_score in [5, 6]
        )

    def _is_match_won(self, player: str) -> bool:
        opponent = self._get_opponent(player)
        sets_won = sum(
            1
            for set_name in ["set1", "set2", "set3"]
            if self.score[set_name][player] > self.score[set_name][opponent]
        )
        return sets_won == 2

    def _start_new_set(self):
        current_set = self._get_current_set()
        next_set = f"set{int(current_set[-1]) + 1}"
        self.score[next_set] = {"player1": 0, "player2": 0}

    @staticmethod
    def _get_opponent(player: str) -> str:
        return "player2" if player == "player1" else "player1"


@dataclass
class MatchList:
    matches: list[Match]
