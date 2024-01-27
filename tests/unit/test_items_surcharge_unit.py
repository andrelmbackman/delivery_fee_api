import pytest
from app.main import items_surcharge
import app.constants as constants


@pytest.mark.parametrize("items", range(5))
def test_no_surcharge(items: int):
    """Test that the surcharge is 0 when the number of items is below 5."""
    assert items_surcharge(items) == 0


@pytest.mark.parametrize("items", range(5, 13))
def test_no_bulk_fee(items: int):
    """Test that the surcharge per number of items over 5 is added."""
    expected_surcharge: int = (
        items - constants.MAX_ITEMS_NO_SURCHARGE
    ) * constants.ADDITIONAL_FEE_PER_ITEM
    assert items_surcharge(items) == expected_surcharge


@pytest.mark.parametrize("items", [13, 14, 15, 20, 50, 100, 1000])
def test_bulk_fee(items: int):
    """Test that the surcharge for each item AND the bulk fee is added."""
    expected_surcharge: int = (
        items - constants.MAX_ITEMS_NO_SURCHARGE
    ) * constants.ADDITIONAL_FEE_PER_ITEM
    expected_surcharge += constants.ITEMS_BULK_FEE
    assert items_surcharge(items) == expected_surcharge
