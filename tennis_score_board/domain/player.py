from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    id: Optional[int]
    name: str
