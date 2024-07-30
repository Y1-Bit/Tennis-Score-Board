from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String
from app.database.database import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
