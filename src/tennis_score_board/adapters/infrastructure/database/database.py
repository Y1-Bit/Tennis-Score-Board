from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from tennis_score_board.config import Config

Base = declarative_base()


class Database:
    def __init__(self, config: Config):
        self.engine = create_engine(config.db.get_connection_string())
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def get_db(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()


def init_database(config: Config):
    return Database(config)
