import uuid

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from tennis_score_board.database.database import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    player1_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    winner_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.id"), nullable=True
    )
    score: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    def __init__(self, player1_id: int, player2_id: int) -> None:
        self.uuid = str(uuid.uuid4())
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score = None
        self.winner_id = None

    def __repr__(self) -> str:
        return f"<Match(id={self.id}, uuid='{self.uuid}', player1_id={self.player1_id}, player2_id={self.player2_id}, winner_id={self.winner_id}, score={self.score})>"
