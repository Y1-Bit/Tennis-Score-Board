import uuid
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Match:
    id: Optional[int]
    uuid: str
    player1_id: int
    player2_id: int
    winner_id: Optional[int]
    score: Optional[Dict[str, int]]

    @classmethod
    def create(cls, player1_id: int, player2_id: int) -> "Match":
        return cls(
            id=None,
            uuid=str(uuid.uuid4()),
            player1_id=player1_id,
            player2_id=player2_id,
            winner_id=None,
            score=None,
        )


@dataclass
class MatchList:
    matches: list[Match]
