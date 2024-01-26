import pytest
from app.main import items_surcharge
import app.constants as const


@pytest.mark.parametrize("items", [0, 1, 2, 3, 4])
def test_no_surcharge(items):
    assert items_surcharge(items) == 0


@pytest.mark.parametrize("items", [5, 6, 7, 8, 9, 10, 11, 12])
def test_no_bulk_fee(items):
    expected_surcharge = (
        items - const.MAX_ITEMS_NO_SURCHARGE
    ) * const.ADDITIONAL_FEE_PER_ITEM
    assert items_surcharge(items) == expected_surcharge


@pytest.mark.parametrize("items", [13, 14, 15, 20, 50, 100, 1000])
def test_bulk_fee(items):
    expected_surcharge = (
        items - const.MAX_ITEMS_NO_SURCHARGE
    ) * const.ADDITIONAL_FEE_PER_ITEM
    expected_surcharge += const.ITEMS_BULK_FEE
    assert items_surcharge(items) == expected_surcharge
