from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from config import DatabaseSettings


class Snowflake:
    """
    Represents a connection to a Snowflake database.
    """

    engine: Engine
    session_local: sessionmaker

    def __init__(self, config: DatabaseSettings) -> None:
        self.engine = create_engine(config.db_connection_uri, pool_pre_ping=True)
        self.session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )


def get_db(database: Snowflake):
    """
    Return a database session.
    """

    db = database.session_local()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
