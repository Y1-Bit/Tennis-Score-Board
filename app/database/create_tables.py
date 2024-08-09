from app.database.database import Base, engine
from app.models import *

Base.metadata.create_all(bind=engine)
