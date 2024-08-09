from sqlalchemy.orm import Session

from tennis_score_board.exceptions import MatchNotFoundError
from tennis_score_board.models.match import Match
from tennis_score_board.services.interfaces import MatchRepoInterface


class MatchRepo(MatchRepoInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, match: Match) -> Match:
        self.db_session.add(match)
        self.db_session.commit()
        self.db_session.refresh(match)
        return match

    def get_all(self) -> list[Match]:
        return self.db_session.query(Match).all()

    def get_by_id(self, match_id: int) -> Match:
        match = self.db_session.query(Match).filter(Match.id == match_id).first()
        if match is None:
            raise MatchNotFoundError(match_id)
        return match
