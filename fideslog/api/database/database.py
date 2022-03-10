from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from fideslog.api.config import config

engine = create_engine(config.database.db_connection_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    """
    Return a database session.
    """

    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
