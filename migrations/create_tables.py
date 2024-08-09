from tennis_score_board.database.database import Base, engine
from tennis_score_board.models import *

Base.metadata.create_all(bind=engine)
