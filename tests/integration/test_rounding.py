from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from tests.conftest import API_ENDPOINT


"""
Tests that ensure that rounding is handled properly. Since the
rush hour multiplier is 1.2, only decimals of .2, .4, .6, and .8 are generated.
"""


def test_round_down_dot_two():
    """Test rounding down for a fractional value ending in .2"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 999,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 241} # 241.2
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


def test_round_down_dot_four():
    """Test rounding down for a fractional value ending in .4"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 998,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 242} # 242.4
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


def test_round_up_dot_six():
    """Test rounding up for a fractional value ending in .6"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 997,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 244} # 243.6
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


def test_round_up_dot_eight():
    """"Test rounding up for a fractional value ending in .8"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 996,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 245} # 244.8
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response
