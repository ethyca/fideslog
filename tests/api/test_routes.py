import pytest
from fastapi import status
from fastapi.testclient import TestClient

from fideslog.api.main import app

client = TestClient(app)


@pytest.mark.skip(
    "Starlette test client breaks in this FastAPI version. We either need to upgrade the version, or more likely, deprecate fideslog entirely."
)
def test_health() -> None:
    """Test that the /health endpoint responds"""

    response = client.get("/health", headers={"X-Fideslog-Version": "1.0.0"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
