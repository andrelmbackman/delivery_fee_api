from fastapi.testclient import TestClient
import pytest
import math
from app.main import app
from app.error_messages import INVALID_TIME_FORMAT

API_ENDPOINT = "/delivery_fee"


def test_empty_request_body():
    """Ensure that empty request bodies raise an error response."""
    with TestClient(app) as client:
        response = client.post(API_ENDPOINT)
        assert response.status_code == 422

@pytest.mark.parametrize("payload", [
    {"cart_value": 0},
    {"cart_value": 0, "delivery_distance": 0},
    {"delivery_distance": 0, "number_of_items": 1},
    {"delivery_distance": 0, "time": "2024-01-26T16:00:00Z"},
])
def test_invalid_request_body(payload):
    """Ensure that incomplete request bodies cause an error response code."""
    with TestClient(app) as client:
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 422


def test_invalid_keys():
    """Test that incomplete keys raise an error response.."""
    with TestClient(app) as client:
        payload = {
            "value": 790,
            "distance": 2235,
            "items": 4,
            "time": "2024-01-15T13:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 422

@pytest.mark.parametrize("value", [-1, -100, -999, -2147483648])
def test_invalid_cart_value(value: int):
    """Test that negative cart values raise an error response."""
    with TestClient(app) as client:
        payload = {
            "cart_value": value,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 422

@pytest.mark.parametrize("distance", [-1, -9, -99, -999, -99999999999999999999])
def test_invalid_distance(distance: int):
    """Test that negative distances raise an error response."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": distance,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 422

@pytest.mark.parametrize("items", [0, -9, -99, -999, -99999999999999999999])
def test_invalid_items(items: int):
    """Test that non-positive item numbers raise an error response."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": items,
            "time": "2024-01-26T16:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 422


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
    """Test that invalid time formats raise an error response."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": time,
        }
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 400
        assert INVALID_TIME_FORMAT in response.json()["detail"]


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
        {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 1,
            "time": 2024,
        },
    ],
)
def test_invalid_data_types(payload):
    """Test that correct data types are enforced."""
    with TestClient(app) as client:
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 422


def test_valid_request():
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        }
        expected_response = {"delivery_fee": 710}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json() == expected_response


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
    with TestClient(app) as client:
        payload = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": time,
        }
        expected_response = {"delivery_fee": 852}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json() == expected_response


def test_rush_hour_minimum_distance():
    """Test that the rush hour multiplier is applied to the lowest delivery fee."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 1000,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        expected_response = {"delivery_fee": 240}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json() == expected_response


def test_rush_hour_minimum_distance_cart_surcharge():
    """Test the rush hour multiplier with cart_value surcharge"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 990,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        expected_response = {"delivery_fee": 252}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json() == expected_response


def test_rush_hour_minimum_distance_5_items():
    """Test rush hour multiplier with one additional item surcharge."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 1000,
            "delivery_distance": 500,
            "number_of_items": 5,
            "time": "2024-01-26T16:00:00Z",
        }
        expected_response = {"delivery_fee": 300}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
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
    assert response.status_code == 200
    assert response.json() == expected_response


def test_valid_cheap_order():
    with TestClient(app) as client:
        payload = {
            "cart_value": 1000,
            "delivery_distance": 999,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        }
        expected_response = {"delivery_fee": 200}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.parametrize("value", [20000, 50000, 100000, 9999999])
def test_free_delivery(value: int):
    """
    Make sure that the delivery fee is 0 when cart_value exceeds 20000.
    Items surcharge, bulk fees, rush hour, delivery distance disregarded.
    """
    with TestClient(app) as client:
        payload = {
            "cart_value": value,
            "delivery_distance": 5000,
            "number_of_items": 100,
            "time": "2024-01-16T17:00:00Z",
        }
        expected_response = {"delivery_fee": 0}
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 200
        assert response.json() == expected_response

@pytest.mark.parametrize("distance", [20000, 50000, 9999999, 99999999999])
def test_max_delivery_fee(distance: int):
    """Test that the delivery fee never exceeds 1500"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 0,
            "delivery_distance": distance,
            "number_of_items": 1000,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 1500}
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 200
        assert response.json() == expected_response


def test_small_value_big_distance():
    with TestClient(app) as client:
        payload = {
            "cart_value": 10,
            "delivery_distance": 20000,
            "number_of_items": 4,
            "time": "2024-01-23T23:00:00Z",
        }
        expected_response = {"delivery_fee": 1500}
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.parametrize("value", range(0, 1001, 10))
def test_cart_values(value: int):
    """Test all cart values ranging from 0-1000 in intervals of 10."""
    client = TestClient(app)
    payload = {
        "cart_value": value,
        "delivery_distance": 200,
        "number_of_items": 4,
        "time": "2024-01-23T23:00:00Z",
    }
    expected_fee: int = 1000 - value + 200
    expected_response = {"delivery_fee": expected_fee}
    response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.parametrize("distance", range(501, 7002, 500))
def test_delivery_distance(distance: int):
    """Test full range of delivery distance fee."""
    client = TestClient(app)
    payload = {
        "cart_value": 1000,
        "delivery_distance": distance,
        "number_of_items": 4,
        "time": "2024-01-23T23:00:00Z",
    }
    expected_fee: int = 100 * math.ceil(
        distance / 500
    )  # starts at 200, no need to add starting fee
    expected_response = {"delivery_fee": expected_fee}
    response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.parametrize("items", range(5, 26, 1))
def test_number_of_items(items: int):
    """Test the full range of the items surcharge."""
    client = TestClient(app)
    payload = {
        "cart_value": 1000,
        "delivery_distance": 1000,
        "number_of_items": items,
        "time": "2024-01-23T23:00:00Z",
    }
    expected_fee: int = min(200 + ((items - 4) * 50) + (120 if items > 12 else 0), 1500)
    expected_response = {"delivery_fee": expected_fee}
    response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == 200
    assert response.json() == expected_response
