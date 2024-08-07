from sqlalchemy.orm import Session

from app.models.player import Player
from app.repositories.interfaces import PlayerRepoInterface


class PlayerRepo(PlayerRepoInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_or_create(self, player_name: str) -> Player:
        player = (
            self.db_session.query(Player).filter(Player.name == player_name).first()
        )
        if player is None:
            player = Player(name=player_name)
            self.db_session.add(player)
            self.db_session.commit()
        return player