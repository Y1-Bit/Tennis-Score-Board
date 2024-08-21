from sqlalchemy.orm import Session

from tennis_score_board.adapters.infrastructure.models import Player as DBPlayer
from tennis_score_board.application.interfaces import PlayerRepoInterface
from tennis_score_board.domain.player import Player as DomainPlayer


class PlayerRepo(PlayerRepoInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_or_create(self, player_name: str) -> DomainPlayer:
        db_player = (
            self.db_session.query(DBPlayer).filter(DBPlayer.name == player_name).first()
        )
        if db_player is None:
            db_player = DBPlayer(name=player_name)
            self.db_session.add(db_player)
        return self._to_domain(db_player)

    def _to_domain(self, db_player: DBPlayer) -> DomainPlayer:
        return DomainPlayer(id=db_player.id, name=db_player.name)
