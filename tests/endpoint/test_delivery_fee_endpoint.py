from fastapi.testclient import TestClient
from fastapi import status
import pytest
import math
from app.main import app
from app.constants import OrderConstants
from tests.conftest import API_ENDPOINT


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
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


def test_rush_hour_minimum_distance():
    """Test if the rush hour multiplier is applied to the lowest delivery fee."""
    with TestClient(app) as client:
        payload = {
            "cart_value": 1000,
            "delivery_distance": 500,
            "number_of_items": 4,
            "time": "2024-01-26T16:00:00Z",
        }
        expected_response = {"delivery_fee": 240}
        response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_200_OK
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
    assert response.status_code == status.HTTP_200_OK
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
    assert response.status_code == status.HTTP_200_OK
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
    assert response.status_code == status.HTTP_200_OK
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
        assert response.status_code == status.HTTP_200_OK
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
        assert response.status_code == status.HTTP_200_OK
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
        assert response.status_code == status.HTTP_200_OK
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
    assert response.status_code == status.HTTP_200_OK
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
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


def calculate_expected_fee(items: int) -> int:
    """
    Helper function for test_number_of_items.
    Calculate the expected delivery fee based on the number of items.

    Args:
        items (int): The number of items in the order.

    Returns:
        int: The expected delivery fee in cents.
    """
    starting_fee: int = OrderConstants.DISTANCE_STARTING_FEE
    additional_items: int = max(items - OrderConstants.MAX_ITEMS_NO_SURCHARGE, 0)
    item_surcharge: int = additional_items * OrderConstants.ADDITIONAL_FEE_PER_ITEM
    bulk_fee = 120 if items > 12 else 0
    return min(starting_fee + item_surcharge + bulk_fee, 1500)


@pytest.mark.parametrize("items", range(5, 26, 1))
def test_number_of_items(items: int):
    """Test the full range of the items surcharge."""
    client = TestClient(app)
    payload = {
        "cart_value": 1000,
        "delivery_distance": 500,
        "number_of_items": items,
        "time": "2024-01-23T23:00:00Z",
    }
    expected_fee: int = calculate_expected_fee(items)
    expected_response = {"delivery_fee": expected_fee}
    response = client.post(API_ENDPOINT, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

