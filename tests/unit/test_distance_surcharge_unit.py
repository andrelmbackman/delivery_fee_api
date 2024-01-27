import pytest
from app.main import distance_surcharge
from app.constants import DISTANCE_STARTING_FEE, DISTANCE_HALF_KM_FEE, STARTING_DISTANCE

@pytest.mark.parametrize("distance", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_low_distance(distance: int):
    """Test if the surcharge actually starts at the starting fee."""
    assert distance_surcharge(distance) == DISTANCE_STARTING_FEE


@pytest.mark.parametrize("subtrahend", [100, 200, 333, 444, 575, 750, 870, 999])
def test_distance_below_starting_distance(subtrahend: int):
    """Test if the surcharge actually starts at the starting fee."""
    distance: int = STARTING_DISTANCE - subtrahend
    assert distance_surcharge(distance) == DISTANCE_STARTING_FEE


def test_starting_distance():
    """Test if the surcharge actually starts at the starting fee."""
    assert distance_surcharge(STARTING_DISTANCE) == DISTANCE_STARTING_FEE


@pytest.mark.parametrize("multiplier", [1, 2, 3, 4, 5, 6, 7, 8, 9, 25, 50, 999])
def test_above_starting_distance(multiplier: int):
    """Validate that the right distance surcharge is added."""
    added_distance: int = STARTING_DISTANCE + (multiplier * 500)
    expected_surcharge: int = DISTANCE_STARTING_FEE + (
        multiplier * DISTANCE_HALF_KM_FEE
    )
    assert distance_surcharge(added_distance) == expected_surcharge
