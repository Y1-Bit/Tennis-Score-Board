from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.tennis_score_board.config import Config, load_config

config: Config = load_config(".env")
database_url = config.db.get_connection_string()

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
