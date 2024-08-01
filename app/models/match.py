from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, ForeignKey, JSON
from app.database.database import Base


class Matches(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    player1_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    winner_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    score: Mapped[dict] = mapped_column(JSON, nullable=False)

    def __repr__(self) -> str:
        return f"<Match(id={self.id}, uuid='{self.uuid}', player1_id={self.player1_id}, player2_id={self.player2_id}, winner_id={self.winner_id}, score={self.score})>"
