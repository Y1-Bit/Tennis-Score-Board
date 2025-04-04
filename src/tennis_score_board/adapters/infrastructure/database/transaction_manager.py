from contextlib import contextmanager

from sqlalchemy.orm import Session

from tennis_score_board.application.interfaces import TransactionManagerInterface


class TransactionManager(TransactionManagerInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @contextmanager
    def transaction(self):
        try:
            yield
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
