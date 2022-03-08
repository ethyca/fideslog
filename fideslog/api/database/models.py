from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Sequence,
    String,
)

from fideslog.api.database.database import Base


class UtcNow(expression.FunctionElement):  # pylint: disable=too-many-ancestors
    """Defines the use of a default load of a UTC timestamp"""

    type = DateTime()
    inherit_cache = True


@compiles(UtcNow, "snowflake")
def sf_utcnow(
    element: Column, compiler: str, **kw: dict  # pylint: disable=unused-argument
) -> str:
    """Defines the use of a default load of a UTC timestamp"""
    return "sysdate()"


class AnalyticsEvent(Base):
    """
    The persisted details about an analytics event.
    """

    __tablename__ = "ANONYMOUS_USAGE_EVENTS"

    id = Column("EVENT_ID", Integer, Sequence("event_id_seq"), primary_key=True)
    client_id = Column("CLIENT_ID", String, default=None, nullable=True)
    product_name = Column("PRODUCT_NAME", String, default=None, nullable=True)
    production_version = Column(
        "PRODUCTION_VERSION", String, default=None, nullable=True
    )
    os = Column("OS", String, default=None, nullable=True)
    docker = Column("DOCKER", Boolean, default=None, nullable=True)
    resource_counts = Column("RESOURCE_COUNTS", String, default=None, nullable=True)
    event = Column("EVENT", String, default=None, nullable=True)
    command = Column("COMMAND", String, default=None, nullable=True)
    flags = Column("FLAGS", String, default=None, nullable=True)
    endpoint = Column("ENDPOINT", String, default=None, nullable=True)
    status_code = Column("STATUS_CODE", Integer, default=None, nullable=True)
    error = Column("ERROR", String, default=None, nullable=True)
    local_host = Column("LOCAL_HOST", Boolean, default=None, nullable=True)
    extra_data = Column("EXTRA_DATA", String, default=None, nullable=True)
    event_created_at = Column(
        "EVENT_CREATED_AT", DateTime(timezone=True), default=None, nullable=True
    )
    event_loaded_at = Column(
        "EVENT_LOADED_AT", DateTime(timezone=True), server_default=UtcNow()
    )


class APIKey(Base):
    """
    The persisted details about API access keys.
    """

    __tablename__ = "API_KEYS"

    id = Column("ID", Integer, Sequence("keys_id_seq"), primary_key=True)
    api_key = Column("API_KEY", String, default=None, nullable=True)
    client_id = Column("CLIENT_ID", String, default=None, nullable=True)
    created_at = Column(
        "CREATED_AT", DateTime(timezone=True), default=None, nullable=True
    )
    expired_at = Column(
        "EXPIRED_AT", DateTime(timezone=True), default=None, nullable=True
    )


class CLIAPIMapping(Base):
    """
    The persisted details mapping a CLI instance to an API instance.
    """

    __tablename__ = "CLI_API_MAPPING"

    id = Column("ID", Integer, Sequence("mapping_id_seq"), primary_key=True)
    api_id = Column("API_ID", String, default=None, nullable=True)
    cli_id = Column("CLI_ID", String, default=None, nullable=True)
    created_at = Column(
        "CREATED_AT", DateTime(timezone=True), default=None, nullable=True
    )
    updated_at = Column(
        "UPDATED_AT", DateTime(timezone=True), default=None, nullable=True
    )
