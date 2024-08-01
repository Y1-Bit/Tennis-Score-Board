from sqlalchemy.orm import Session

from app.models.player import Player


def get_or_create_player(db: Session, player_name: str) -> Player:
    player = db.query(Player).filter(Player.name == player_name).one_or_none()
    if player is None:
        player = Player(name=player_name)
        db.add(player)
        db.commit()
    return player
