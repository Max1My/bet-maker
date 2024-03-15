from starlette import status
from starlette.testclient import TestClient
from main import app

client = TestClient(app)

route = '/api/v1/bets/'


def test_create_bets():
    response = client.post(
        url=route,
        headers={"Content-Type": "application/json"},
        json={
          "event_id": 1,
          "bet_amount": -0.15
        }
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text


def test_read_bets():
    response = client.get(
        url=f'{route}/',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == status.HTTP_200_OK, response.text
