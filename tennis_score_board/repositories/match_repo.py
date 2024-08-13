from sqlalchemy.orm import Session

from tennis_score_board.domain.match import Match as DomainMatch
from tennis_score_board.domain.match import MatchList as DomainMatchList
from tennis_score_board.exceptions import MatchNotFoundError
from tennis_score_board.models.match import Match as DBMatch
from tennis_score_board.models.player import Player as DBPlayer
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
        )

    def add(self, match: DomainMatch) -> DomainMatch:
        db_match = DBMatch(
            uuid=match.uuid,
            player1_id=match.player1_id,
            player2_id=match.player2_id,
            winner_id=match.winner_id,
            score=match.score,
        )
        self.db_session.add(db_match)
        return self._to_domain(db_match)

    def update(self, match: DomainMatch) -> DomainMatch:
        db_match = (
            self.db_session.query(DBMatch).filter(DBMatch.uuid == match.uuid).first()
        )
        if db_match is None:
            raise MatchNotFoundError(match.uuid)
        db_match.winner_id = match.winner_id
        db_match.score = match.score
        return self._to_domain(db_match)

    def get_all(self) -> DomainMatchList:
        db_matches = self.db_session.query(DBMatch).all()
        domain_matches = [self._to_domain(match) for match in db_matches]
        return DomainMatchList(matches=domain_matches)

    def get_by_uuid(self, uuid: str) -> DomainMatch:
        match = self.db_session.query(DBMatch).filter(DBMatch.uuid == uuid).first()
        if match is None:
            raise MatchNotFoundError(uuid)
        return self._to_domain(match)

    def get_matches(
        self, page: int, filter_by_player_name: str | None = None, per_page: int = 10
    ) -> tuple[list[DomainMatch], int]:
        query = self.db_session.query(DBMatch)

        if filter_by_player_name:
            query = query.join(
                DBPlayer,
                (DBMatch.player1_id == DBPlayer.id)
                | (DBMatch.player2_id == DBPlayer.id),
            ).filter(DBPlayer.name == filter_by_player_name)

        total = query.count()
        matches = (
            query.order_by(DBMatch.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return [self._to_domain(m) for m in matches], (total + per_page - 1) // per_page
