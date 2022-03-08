from fastapi import status
from fastapi.testclient import TestClient

from fideslog.api.main import app

client = TestClient(app)


def test_health() -> None:
    """Test that the /health endpoint responds"""

    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
