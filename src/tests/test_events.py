from starlette import status
from starlette.testclient import TestClient

from main import app

from src.core.domain.events import requests

client = TestClient(app)

route = '/api/v1/events/'


def test_update_activity_type():
    request = requests.UpdateStatusEventRequest(
        status="LOSE",
    ).model_dump()
    response = client.put(
        url=f'{route}/1',
        headers={"Content-Type": "application/json"},
        json=request
    )
    assert response.status_code == status.HTTP_200_OK, response.text
