import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GameScore:
    player1: int = 0
    player2: int = 0


@dataclass
class SetScore:
    player1: int = 0
    player2: int = 0


@dataclass
class MatchScore:
    current_game: GameScore = field(default_factory=GameScore)
    set1: SetScore = field(default_factory=SetScore)
    set2: SetScore = field(default_factory=SetScore)
    set3: SetScore = field(default_factory=SetScore)


@dataclass
class Match:
    id: Optional[int] = None
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    player1_id: int | None = None
    player2_id: int | None = None
    winner_id: Optional[int] = None
    score: MatchScore = field(default_factory=MatchScore)

    @classmethod
    def create(cls, player1_id: int, player2_id: int) -> "Match":
        return cls(player1_id=player1_id, player2_id=player2_id)

    @property
    def is_finished(self) -> bool:
        return self.winner_id is not None

    def add_point(self, player: str):
        if self.is_finished:
            raise ValueError("Match is already finished")
        
        current_set = self._get_current_set()
        if player == "player1":
            self.score.current_game.player1 += 1
        else:
            self.score.current_game.player2 += 1

        if self._is_game_won(player):
            setattr(current_set, player, getattr(current_set, player) + 1)
            self._reset_game_score()
            if self._is_set_won(player, current_set):
                if self._is_match_won(player):
                    self.winner_id = self.player1_id if player == "player1" else self.player2_id
                else:
                    self._start_new_set()

    def _get_current_set(self) -> SetScore:
        for set_name in ["set1", "set2", "set3"]:
            set_score = getattr(self.score, set_name)
            if set_score.player1 < 6 and set_score.player2 < 6:
                return set_score
        raise ValueError("All sets are finished")

    def _is_game_won(self, player: str) -> bool:
        player_score = getattr(self.score.current_game, player)
        opponent_score = getattr(self.score.current_game, self._get_opponent(player))
        return player_score >= 4 and player_score - opponent_score >= 2

    def _reset_game_score(self):
        self.score.current_game = GameScore()

    def _is_set_won(self, player: str, current_set: SetScore) -> bool:
        player_score = getattr(current_set, player)
        opponent_score = getattr(current_set, self._get_opponent(player))
        return (player_score == 6 and opponent_score <= 4) or (player_score == 7 and opponent_score in [5, 6])

    def _is_match_won(self, player: str) -> bool:
        opponent = self._get_opponent(player)
        sets_won = sum(
            1 for set_name in ["set1", "set2", "set3"]
            if getattr(getattr(self.score, set_name), player) > getattr(getattr(self.score, set_name), opponent)
        )
        return sets_won == 2

    def _start_new_set(self):
        if self.score.set2.player1 == 0 and self.score.set2.player2 == 0:
            self.score.set2 = SetScore()
        elif self.score.set3.player1 == 0 and self.score.set3.player2 == 0:
            self.score.set3 = SetScore()
        else:
            raise ValueError("Cannot start a new set, all sets are used")

    @staticmethod
    def _get_opponent(player: str) -> str:
        return "player2" if player == "player1" else "player1"

@dataclass
class MatchList:
    matches: list[Match]