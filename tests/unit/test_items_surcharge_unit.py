import pytest
from app.delivery_fee import items_surcharge
from app.constants import OrderConstants


max_items_no_surcharge: int = OrderConstants.MAX_ITEMS_NO_SURCHARGE
additional_fee_per_item: int = OrderConstants.ADDITIONAL_FEE_PER_ITEM
bulk_fee: int = OrderConstants.ITEMS_BULK_FEE


@pytest.mark.parametrize("items", range(5))
def test_no_surcharge(items: int):
    """Test that the surcharge is 0 when the number of items is below 5."""
    assert items_surcharge(items) == 0


@pytest.mark.parametrize("items", range(5, 13))
def test_no_bulk_fee(items: int):
    """Test that the surcharge per number of items over 5 is added."""
    expected_surcharge: int = (items - max_items_no_surcharge) * additional_fee_per_item
    assert items_surcharge(items) == expected_surcharge


@pytest.mark.parametrize("items", [13, 14, 15, 20, 50, 100, 1000])
def test_bulk_fee(items: int):
    """Test that the surcharge for each item AND the bulk fee is added."""
    expected_surcharge: int = (items - max_items_no_surcharge) * additional_fee_per_item
    expected_surcharge += bulk_fee
    assert items_surcharge(items) == expected_surcharge
