from sqlalchemy import (
    create_engine,
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from sqlalchemy.ext.declarative import declarative_base

from decouple import config

DATABASE_URL = config("DATABASE_URL")


ENGINE = create_engine(DATABASE_URL, echo=True)
session_factory = sessionmaker(bind=ENGINE)
SESSION = scoped_session(session_factory)
BASE = declarative_base()
