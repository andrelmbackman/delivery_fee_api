import pytest
from app.main import distance_surcharge
import app.constants as const


# Test if the surcharge actually starts at the starting fee
def test_low_distance():
    assert distance_surcharge(0) == const.DISTANCE_STARTING_FEE
    assert distance_surcharge(1) == const.DISTANCE_STARTING_FEE
    assert distance_surcharge(5) == const.DISTANCE_STARTING_FEE
    assert distance_surcharge(10) == const.DISTANCE_STARTING_FEE


def test_distance_below_starting_distance():
    distance = const.STARTING_DISTANCE - 100
    assert distance_surcharge(distance) == const.DISTANCE_STARTING_FEE
    distance = const.STARTING_DISTANCE - 500
    assert distance_surcharge(distance) == const.DISTANCE_STARTING_FEE
    distance = const.STARTING_DISTANCE - 750
    assert distance_surcharge(distance) == const.DISTANCE_STARTING_FEE


def test_starting_distance():
    assert distance_surcharge(const.STARTING_DISTANCE) == const.DISTANCE_STARTING_FEE


# Test if the right fee is added
@pytest.mark.parametrize("multiplier", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_above_starting_distance(multiplier):
    added_distance = const.STARTING_DISTANCE + (multiplier * 500)
    expected_surcharge = const.DISTANCE_STARTING_FEE + (
        multiplier * const.DISTANCE_HALF_KM_FEE
    )
    assert distance_surcharge(added_distance) == expected_surcharge
