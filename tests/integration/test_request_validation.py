import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.constants import ErrorMessages
from tests.conftest import API_ENDPOINT


def test_empty_request_body():
    """Ensure that empty request bodies raise an error response."""
    with TestClient(app) as client:
        response = client.post(API_ENDPOINT)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_forbidden_request_types():
    """Ensure that other request types than POST get a proper error response."""
    with TestClient(app) as client:
        response = client.get(API_ENDPOINT)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = client.head(API_ENDPOINT)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = client.put(API_ENDPOINT)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = client.delete(API_ENDPOINT)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = client.options(API_ENDPOINT)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = client.patch(API_ENDPOINT)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "payload",
    [
        {"cart_value": 0},
        {"cart_value": 0, "delivery_distance": 0},
        {"delivery_distance": 0, "number_of_items": 1},
        {"delivery_distance": 0, "time": "2024-01-26T16:00:00Z"},
    ],
)
def test_invalid_request_body(payload):
    """Ensure that incomplete request bodies cause an error response."""
    with TestClient(app) as client:
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_invalid_keys():
    """Test that incomplete keys cause an error response.."""
    with TestClient(app) as client:
        payload = {
            "value": 790,
            "distance": 2235,
            "items": 4,
            "time": "2024-01-15T13:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("value", [-1, -100, -999, -2147483648])
def test_invalid_cart_value(value: int):
    """Test that negative cart values cause an error response."""
    with TestClient(app) as client:
        payload = {
            "cart_value": value,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("distance", [-1, -9, -99, -999, -99999999999999999999])
def test_invalid_distance(distance: int):
    """Test that negative distances cause an error response."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": distance,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("items", [0, -9, -99, -999, -99999999999999999999])
def test_invalid_items(items: int):
    """Test that non-positive item numbers cause an error response."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": items,
            "time": "2024-01-26T16:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "time",
    [
        "24-01-26T17:00:45Z",
        "9999-99-99T17:00:45Z",
        "2024-01-01T99:99:99.999Z",
        "2020-0-15Ö00:00:00Q",
        "0-01-15T13:00:00",
        "2023-x-y5T13:00:00",
        "2024-01-26T17:00:45+00Z",
        "2024-01-26T17:00:45-00Z",
        "2024-01-26T17:00",
    ],
)
def test_invalid_time_formats(time: str):
    """Test that invalid time formats cause an error response."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": time,
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert ErrorMessages.INVALID_TIME_FORMAT in response.json()["detail"]


@pytest.mark.parametrize(
    "payload",
    [
        {
            "cart_value": "1000",
            "delivery_distance": 1000,
            "number_of_items": 1,
            "time": "2024-01-23T17:00:45Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": "1000",
            "number_of_items": 1,
            "time": "2024-01-23T17:00:45Z",
        },
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": "1",
            "time": "2024-01-23T17:00:45Z",
        },
    ],
)
def test_invalid_data_types(payload):
    """Test that correct data types are enforced."""
    with TestClient(app) as client:
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
