from sqlalchemy.orm import Session

from tennis_score_board.adapters.infrastructure.models import Match as DBMatch
from tennis_score_board.adapters.infrastructure.models import Player as DBPlayer
from tennis_score_board.application.interfaces import MatchRepoInterface
from tennis_score_board.domain.match import GameScore
from tennis_score_board.domain.match import Match as DomainMatch
from tennis_score_board.domain.match import Player as DomainPlayer
from tennis_score_board.domain.match import MatchList as DomainMatchList
from tennis_score_board.domain.match import MatchScore, SetScore
from tennis_score_board.exceptions import MatchNotFoundError


class MatchRepo(MatchRepoInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def _to_player(self, db_player: DBPlayer) -> DomainPlayer:
        return DomainPlayer(id=db_player.id, name=db_player.name)

    def _to_domain(self, db_match: DBMatch) -> DomainMatch:
        return DomainMatch(
            id=db_match.id,
            uuid=db_match.uuid,
            player1=db_match.player1,
            player2=db_match.player2,
            winner_id=db_match.winner_id,
            score=MatchScore(
                current_game=GameScore(
                    db_match.current_game_player1, db_match.current_game_player2
                ),
                set1=SetScore(db_match.set1_player1, db_match.set1_player2),
                set2=SetScore(db_match.set2_player1, db_match.set2_player2),
                set3=SetScore(db_match.set3_player1, db_match.set3_player2),
            ),
        )

    def _to_db(self, match: DomainMatch, player1: DomainPlayer, player2: DomainPlayer) -> DBMatch:
        return DBMatch(
            id=match.id,
            uuid=match.uuid,
            player1_id=player1.id,
            player2_id=player2.id,
            winner_id=match.winner_id,
            current_game_player1=match.score.current_game.player1,
            current_game_player2=match.score.current_game.player2,
            set1_player1=match.score.set1.player1,
            set1_player2=match.score.set1.player2,
            set2_player1=match.score.set2.player1,
            set2_player2=match.score.set2.player2,
            set3_player1=match.score.set3.player1,
            set3_player2=match.score.set3.player2,
        )

    def add(self, match: DomainMatch, player1: DomainPlayer, player2: DomainPlayer) -> DomainMatch:
        db_match = self._to_db(match, player1, player2)
        self.db_session.add(db_match)
        return self._to_domain(db_match)

    def update(self, match: DomainMatch) -> DomainMatch:
        db_match = (
            self.db_session.query(DBMatch).filter(DBMatch.uuid == match.uuid).first()
        )
        if db_match is None:
            raise MatchNotFoundError(match.uuid)

        db_match.winner_id = match.winner_id
        db_match.current_game_player1 = match.score.current_game.player1
        db_match.current_game_player2 = match.score.current_game.player2
        db_match.set1_player1 = match.score.set1.player1
        db_match.set1_player2 = match.score.set1.player2
        db_match.set2_player1 = match.score.set2.player1
        db_match.set2_player2 = match.score.set2.player2
        db_match.set3_player1 = match.score.set3.player1
        db_match.set3_player2 = match.score.set3.player2

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
