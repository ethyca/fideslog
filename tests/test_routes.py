import pytest

import requests


LOCAL_SERVER_URL = "http://fideslog:8080"


def test_health():
    response = requests.get(f"{LOCAL_SERVER_URL}/health")

    assert response.status_code == 200
