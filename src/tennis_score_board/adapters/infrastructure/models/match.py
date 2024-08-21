from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from tennis_score_board.adapters.infrastructure.database import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    player1_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    winner_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("players.id"), nullable=True
    )
    current_game_player1: Mapped[int] = mapped_column(Integer, default=0)
    current_game_player2: Mapped[int] = mapped_column(Integer, default=0)
    set1_player1: Mapped[int] = mapped_column(Integer, default=0)
    set1_player2: Mapped[int] = mapped_column(Integer, default=0)
    set2_player1: Mapped[int] = mapped_column(Integer, default=0)
    set2_player2: Mapped[int] = mapped_column(Integer, default=0)
    set3_player1: Mapped[int] = mapped_column(Integer, default=0)
    set3_player2: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return f"<Match(id={self.id}, uuid='{self.uuid}', player1_id={self.player1_id}, player2_id={self.player2_id}, winner_id={self.winner_id})>"
