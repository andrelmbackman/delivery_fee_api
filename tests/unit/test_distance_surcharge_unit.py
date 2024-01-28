import pytest
from app.delivery_fee import distance_surcharge
from app.constants import OrderConstants

starting_fee: int = OrderConstants.DISTANCE_STARTING_FEE
half_km_fee: int = OrderConstants.DISTANCE_HALF_KM_FEE
starting_distance: int = OrderConstants.STARTING_DISTANCE


@pytest.mark.parametrize("distance", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_low_distance(distance: int):
    """Test if the surcharge actually starts at the starting fee."""
    assert distance_surcharge(distance) == starting_fee


@pytest.mark.parametrize("subtrahend", [100, 200, 333, 444, 575, 750, 870, 999])
def test_distance_below_starting_distance(subtrahend: int):
    """Test if the surcharge actually starts at the starting fee."""
    distance: int = starting_distance - subtrahend
    assert distance_surcharge(distance) == starting_fee


def test_starting_distance():
    """Test if the surcharge actually starts at the starting fee."""
    assert distance_surcharge(starting_distance) == starting_fee


@pytest.mark.parametrize("multiplier", [1, 2, 3, 4, 5, 6, 7, 8, 9, 25, 50, 999])
def test_above_starting_distance(multiplier: int):
    """Validate that the right distance surcharge is added."""
    added_distance: int = starting_distance + (multiplier * 500)
    expected_surcharge: int = starting_fee + (multiplier * half_km_fee)
    assert distance_surcharge(added_distance) == expected_surcharge
