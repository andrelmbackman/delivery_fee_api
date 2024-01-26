from fastapi.testclient import TestClient
import pytest
import math
from app.main import app
from app.error_messages import (
    INVALID_CART_VALUE,
    INVALID_DELIVERY_DISTANCE,
    INVALID_NUMBER_OF_ITEMS,
    INVALID_TIME_FORMAT,
)

API_ENDPOINT = "/delivery_fee"


def test_empty_request_body():
    with TestClient(app) as client:
        response = client.post(API_ENDPOINT)
        assert response.status_code == 422


def test_invalid_request_body():
    with TestClient(app) as client:
        data = {"cart_value": 790, "delivery_distance": 2235}
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 422


def test_invalid_keys():
    with TestClient(app) as client:
        data = {
            "value": 790,
            "distance": 2235,
            "items": 4,
            "time": "2024-01-15T13:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 422


def test_invalid_distance():
    with TestClient(app) as client:
        data = {
            "cart_value": 790,
            "delivery_distance": -2235,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 400
        assert INVALID_DELIVERY_DISTANCE in response.json()["detail"]


def test_invalid_items():
    with TestClient(app) as client:
        data = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 0,
            "time": "2024-01-26T16:00:00Z",
        }
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 400
        assert INVALID_NUMBER_OF_ITEMS in response.json()["detail"]


@pytest.mark.parametrize("time", [
	"24-01-26T17:00:45Z",
    "2020-0-15Ö00:00:00Q",
    "0-01-15T13:00:00",
    "2023-x-y5T13:00:00",
    "2024-01-26T17:00:45+00Z",
	"2024-01-26T17:00:45-00Z",
    "2024-01-26T17:00"
])
def test_invalid_time_formats(time):
    with TestClient(app) as client:
        data = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": time
        }
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 400
        assert INVALID_TIME_FORMAT in response.json()["detail"]


def test_all_invalid():
    with TestClient(app) as client:
        data = {
            "cart_value": -1,
            "delivery_distance": -1,
            "number_of_items": -4,
            "time": "2020-0-15Ö00:00:00Q",
        }
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 400
        assert INVALID_CART_VALUE in response.json()["detail"]
        assert INVALID_DELIVERY_DISTANCE in response.json()["detail"]
        assert INVALID_NUMBER_OF_ITEMS in response.json()["detail"]
        assert INVALID_TIME_FORMAT in response.json()["detail"]


def test_valid_request():
    with TestClient(app) as client:
        data = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        }
        expected_response = {"delivery_fee": 710}
        response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.parametrize("time", [
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
	"2024-01-26T17:00:45.090-00:00"
])
def test_rush_hour(time):
    with TestClient(app) as client:
        data = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": time,
        }
        expected_response = {"delivery_fee": 852}
        response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response


def test_rush_hour_minimum_distance():
    with TestClient(app) as client:
        data = {
            "cart_value": 1000,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        expected_response = {"delivery_fee": 240}
        response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response

def test_rush_hour_minimum_distance_cart_surcharge():
    with TestClient(app) as client:
        data = {
            "cart_value": 990,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        expected_response = {"delivery_fee": 252}
        response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response

def test_rush_hour_minimum_distance_5_items():
    with TestClient(app) as client:
        data = {
            "cart_value": 1000,
            "delivery_distance": 500,
            "number_of_items": 5,
            "time": "2024-01-26T16:00:00Z",
        }
        expected_response = {"delivery_fee": 300}
        response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response
    
@pytest.mark.parametrize("time", [
	"2024-01-26T17:00:45Z",
	"2024-01-26T12:00:45-05:00",
	"2024-01-26T09:00:45-08:00",
	"2024-01-26T18:00:45+01:00",
	"2024-01-27T02:00:45+09:00"
])
def test_rush_hour_time_zones(time):
    with TestClient(app) as client:
        data = {
            "cart_value": 1000,
            "delivery_distance": 500,
            "number_of_items": 5,
            "time": time,
        }
        expected_response = {"delivery_fee": 300}
        response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response


def test_valid_cheap_order():
    with TestClient(app) as client:
        data = {
            "cart_value": 1000,
            "delivery_distance": 999,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        }
        expected_response = {"delivery_fee": 200}
        response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response


def test_free_delivery():
    with TestClient(app) as client:
        data = {
            "cart_value": 20000,
            "delivery_distance": 500,
            "number_of_items": 1,
            "time": "2024-01-15T13:00:00Z",
        }
        expected_response = {"delivery_fee": 0}
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 200
        assert response.json() == expected_response


def test_max_delivery_fee():
    with TestClient(app) as client:
        data = {
            "cart_value": 100,
            "delivery_distance": 50000,
            "number_of_items": 100,
            "time": "2024-01-15T13:00:00Z",
        }
        expected_response = {"delivery_fee": 1500}
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 200
        assert response.json() == expected_response


def test_small_value_big_distance():
    with TestClient(app) as client:
        data = {
            "cart_value": 10,
            "delivery_distance": 20000,
            "number_of_items": 4,
            "time": "2024-01-23T23:00:00Z",
        }
        expected_response = {"delivery_fee": 1500}
        response = client.post(API_ENDPOINT, json=data)
        assert response.status_code == 200
        assert response.json() == expected_response


# Test all cart values ranging from 10-1000 in intervals of 10.
@pytest.mark.parametrize("value", range(10, 1001, 10))
def test_cart_values(value):
    client = TestClient(app)
    data = {
        "cart_value": value,
        "delivery_distance": 200,
        "number_of_items": 4,
        "time": "2024-01-23T23:00:00Z",
    }
    expected_fee = 1000 - value + 200
    expected_response = {"delivery_fee": expected_fee}
    response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response


# Test full range of delivery distance fee.
@pytest.mark.parametrize("distance", range(501, 7002, 500))
def test_delivery_distance(distance):
    client = TestClient(app)
    data = {
        "cart_value": 1000,
        "delivery_distance": distance,
        "number_of_items": 4,
        "time": "2024-01-23T23:00:00Z",
    }
    expected_fee = 100 * math.ceil(
        distance / 500
    )  # starts at 200, no need to add starting fee
    expected_response = {"delivery_fee": expected_fee}
    response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response


# Test the full range of the items surcharge.
@pytest.mark.parametrize("items", range(5, 26, 1))
def test_number_of_items(items):
    client = TestClient(app)
    data = {
        "cart_value": 1000,
        "delivery_distance": 1000,
        "number_of_items": items,
        "time": "2024-01-23T23:00:00Z",
    }
    expected_fee = min(200 + ((items - 4) * 50) + (120 if items > 12 else 0), 1500)
    expected_response = {"delivery_fee": expected_fee}
    response = client.post(API_ENDPOINT, json=data)
    assert response.status_code == 200
    assert response.json() == expected_response
