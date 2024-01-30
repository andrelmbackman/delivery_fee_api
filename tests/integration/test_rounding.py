from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from tests.conftest import API_ENDPOINT


"""
Tests that ensure that rounding is handled properly. Due to the nature of the
rush hour multiplier, only decimals of .2, .4, .6, and .8 are generated.
"""

def test_round_up_dot_eight():
    """Test if values resulting in a .8 fractional gets rounded up"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 996,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 245} # 244,8
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


def test_round_up_dot_six():
    """Test if values resulting in a .6 fractional gets rounded up"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 997,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 244} # 243,6
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


def test_round_down_dot_four():
    """Test if a .4 fractional gets rounded down"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 998,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 242} # 242,4
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


def test_round_down_dot_two():
    """Test if a .2 fractional gets rounded down"""
    with TestClient(app) as client:
        payload = {
            "cart_value": 999,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T17:00:00Z",
        }
        expected_response = {"delivery_fee": 241} # 241,2
        response = client.post(API_ENDPOINT, json=payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response