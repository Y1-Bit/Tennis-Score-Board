from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.exceptions import MatchNotFoundError
from app.models.match import Match


def add_match(db: Session, match: Match) -> Match:
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_all_matches(db: Session) -> list[Match]:
    return db.query(Match).all()


def get_match_by_id(db: Session, match_id: int) -> Match:
    try:
        return db.query(Match).filter(Match.id == match_id).one()
    except NoResultFound:
        raise MatchNotFoundError(match_id)
