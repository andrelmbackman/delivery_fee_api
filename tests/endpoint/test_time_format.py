from fastapi.testclient import TestClient
from fastapi import status
import pytest
from app.main import app
from tests.conftest import API_ENDPOINT


@pytest.mark.parametrize(
    "time",
    [
        "2024-01-26T17:00:45Z",
        "2024-01-26T18:00:45+01:00",
        "2024-01-26T19:00:45+02:00",
        "2024-01-26T20:00:45+03:00",
        "2024-01-26T21:00:45+04:00",
        "2024-01-26T22:00:45+05:00",
        "2024-01-26T23:00:45+06:00",
        "2024-01-27T00:00:45+07:00",
        "2024-01-27T01:00:45+08:00",
        "2024-01-27T02:00:45+09:00",
        "2024-01-27T03:00:45+10:00",
        "2024-01-27T04:00:45+11:00",
        "2024-01-27T05:00:45+12:00",
        "2024-01-26T16:00:45-01:00",
        "2024-01-26T15:00:45-02:00",
        "2024-01-26T14:00:45-03:00",
        "2024-01-26T13:00:45-04:00",
        "2024-01-26T12:00:45-05:00",
        "2024-01-26T11:00:45-06:00",
        "2024-01-26T10:00:45-07:00",
        "2024-01-26T09:00:45-08:00",
        "2024-01-26T08:00:45-09:00",
        "2024-01-26T07:00:45-10:00",
        "2024-01-26T06:00:45-11:00",
        "2024-01-26T05:00:45-12:00",
        "2024-01-26T17:00:45.000Z",
        "2024-01-26T17:00:45Z",
        "2024-01-26T17:00:45+00",
        "2024-01-26T17:00:45+0000",
        "2024-01-26T17:00:45+00:00",
        "2024-01-26T17:00:45.000+00",
        "2024-01-26T17:00:45.000+0000",
        "2024-01-26T17:00:45.000+00:00",
        "2024-01-26T17:00:45-00",
        "2024-01-26T17:00:45-0000",
        "2024-01-26T17:00:45-00:00",
        "2024-01-26T17:00:45.000-00",
        "2024-01-26T17:00:45.001-0000",
        "2024-01-26T17:00:45.090-00:00",
    ],
)
def test_rush_hour(time: str):
    """Test if the rush hour multiplier is applied using different precisions and timezone offsets."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": time,
        }
        expected_response = {"delivery_fee": 852}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "time",
    [
        "2024-01-26T17:00:45Z",
        "2024-01-26T12:00:45-05:00",
        "2024-01-26T09:00:45-08:00",
        "2024-01-26T18:00:45+01:00",
        "2024-01-27T02:00:45+09:00",
    ],
)
def test_rush_hour_time_zones(time: str):
    """Test that the rush hour multiplier is applied (with timezone offsets)."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 1000,
            "delivery_distance": 500,
            "number_of_items": 5,
            "time": time,
        }
        expected_response = {"delivery_fee": 300}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


