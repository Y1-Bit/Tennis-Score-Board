from sqlalchemy.orm import Session

from app.models.match import Match
from app.repo.match_repo import add_match, get_all_matches
from app.repo.player_repo import get_or_create_player


def create_match(db: Session, form_data: dict) -> Match:
    player1_name = form_data.get("player1_name", [None])[0]
    player2_name = form_data.get("player2_name", [None])[0]

    if not player1_name or not player2_name:
        raise ValueError("Both players must be provided")

    player1 = get_or_create_player(db, player1_name)
    player2 = get_or_create_player(db, player2_name)

    new_match = Match(player1_id=player1.id, player2_id=player2.id)
    return add_match(db, new_match)


def list_matches(db: Session) -> list[Match]:
    return get_all_matches(db)
