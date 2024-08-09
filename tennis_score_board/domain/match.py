from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, List


@dataclass
class Match:
    id: Optional[int]
    uuid: str
    player1_id: int
    player2_id: int
    winner_id: Optional[int]
    score: Optional[Dict[str, int]]
    created_at: datetime


@dataclass
class MatchList:
    matches: List[Match]
