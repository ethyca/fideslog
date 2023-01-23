import logging
from typing import Generator

from boto3 import Session as aws_session
from snowflake.sqlalchemy.snowdialect import SnowflakeDialect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from ..config import config

# Suppress a ton of log output
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

# See: https://github.com/snowflakedb/snowflake-sqlalchemy/issues/265#issuecomment-1026632843
SnowflakeDialect.supports_statement_cache = False

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


def get_storage() -> Generator:
    """
    Return a boto3 session.
    """

    yield aws_session()
