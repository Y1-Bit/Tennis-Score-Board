from sqlalchemy.orm import Session

from tennis_score_board.domain.match import Match as DomainMatch
from tennis_score_board.domain.match import MatchList as DomainMatchList
from tennis_score_board.exceptions import MatchNotFoundError
from tennis_score_board.models.match import Match as DBMatch
from tennis_score_board.services.interfaces import MatchRepoInterface


class MatchRepo(MatchRepoInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _to_domain(self, db_match: DBMatch) -> DomainMatch:
        return DomainMatch(
            id=db_match.id,
            uuid=db_match.uuid,
            player1_id=db_match.player1_id,
            player2_id=db_match.player2_id,
            winner_id=db_match.winner_id,
            score=db_match.score,
            created_at=db_match.created_at,
        )

    def add(self, match: DomainMatch) -> DomainMatch:
        db_match = DBMatch(
            uuid=match.uuid,
            player1_id=match.player1_id,
            player2_id=match.player2_id,
            winner_id=match.winner_id,
            score=match.score,
            created_at=match.created_at,
        )
        self.db_session.add(db_match)
        return self._to_domain(db_match)

    def get_all(self) -> DomainMatchList:
        db_matches = self.db_session.query(DBMatch).all()
        domain_matches = [self._to_domain(match) for match in db_matches]
        return DomainMatchList(matches=domain_matches)

    def get_by_id(self, match_id: int) -> DomainMatch:
        match = self.db_session.query(DBMatch).filter(DBMatch.id == match_id).first()
        if match is None:
            raise MatchNotFoundError(match_id)
        return self._to_domain(match)
