from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from tennis_score_board.adapters.infrastructure.database import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<Player(id={self.id}, name='{self.name}')>"
