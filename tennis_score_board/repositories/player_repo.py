from sqlalchemy.orm import Session

from tennis_score_board.domain.player import Player as DomainPlayer
from tennis_score_board.models.player import Player as DBPlayer
from tennis_score_board.services.interfaces import PlayerRepoInterface


class PlayerRepo(PlayerRepoInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_or_create(self, player_name: str) -> DomainPlayer:
        player = (
            self.db_session.query(DBPlayer).filter(DBPlayer.name == player_name).first()
        )
        if player is None:
            player = DBPlayer(name=player_name)
            self.db_session.add(player)
            self.db_session.commit()
        return player
