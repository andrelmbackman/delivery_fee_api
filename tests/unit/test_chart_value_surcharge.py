import pytest
from app.delivery_fee import cart_value_surcharge
from app.constants import OrderConstants


min_chart_value: int = OrderConstants.MIN_CART_VALUE_NO_SURCHARGE


@pytest.mark.parametrize("value", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_low_chart_value(value: int):
    """
    Test the surcharge calculation for a low chart value.

    Args:
        value (int): The chart value to be tested.

    Description:
    - If the value meets or exceeds the minimum chart value, no surcharge is applied.
    - If the value is below the minimum chart value, the surcharge is calculated as the difference between the minimum chart value and the given value.

    """
    expected_surcharge: int = max(0, min_chart_value - value)
    assert cart_value_surcharge(value) == expected_surcharge


@pytest.mark.parametrize("value", [200, 350, 479, 590, 6, 777, 895, 999])
def test_med_cart_value(value: int):
    """Test the surcharge calculation for a medium chart value."""
    expected_surcharge: int = max(0, min_chart_value - value)
    assert cart_value_surcharge(value) == expected_surcharge


@pytest.mark.parametrize("value", range(1000, 100000, 1000))
def test_high_cart_value(value: int):
    """Test the surcharge calculation for a high chart value."""
    assert cart_value_surcharge(value) == 0
