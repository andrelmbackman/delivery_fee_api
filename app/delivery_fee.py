from datetime import datetime, timezone
from dateutil import parser
import math
from app.models import Order
from app.constants import OrderConstants


def calculate_delivery_fee(order_data: Order) -> int:
    """
    Calculate the full delivery fee of the order.

    Args:
        order_data (Order): The order details including cart value, delivery distance, number of items, and order time.

    Returns:
        float: The total delivery fee in cents.

    Description:
    - If the cart value meets or exceeds the free delivery threshold, the fee is 0.
    - If the cart value is below a certain threshold, a minimum fee is applied.
    - The delivery fee includes surcharges based on the delivery distance and number of items.
    - A rush hour multiplier may apply if the order was placed during rush hours.
    - The delivery fee is capped at a maximum value.
    """
    fee: int = 0

    if order_data.cart_value >= OrderConstants.FREE_DELIVERY_CART_VALUE:
        return 0

    if order_data.cart_value < OrderConstants.NO_SURCHARGE_MIN_CART_VALUE:
        fee = OrderConstants.NO_SURCHARGE_MIN_CART_VALUE - order_data.cart_value

    fee += distance_surcharge(order_data.delivery_distance) + items_surcharge(
        order_data.number_of_items
    )

    if is_rush_hour(order_data.time):
        fee = int(fee * OrderConstants.RUSH_HOUR_MULTIPLIER)

    if fee > OrderConstants.MAX_DELIVERY_FEE:
        return OrderConstants.MAX_DELIVERY_FEE

    return fee


def distance_surcharge(distance: int) -> int:
    """
    Calculate the delivery surcharge based on the given distance (in meters).

    Args:
        distance (int): The delivery distance in meters.

    Returns:
        int: The surcharge amount in cents.

    The surcharge starts at 200 cents for the first 1000 meters.
    For every additional 500 meters started beyond the first 1000 meters, 100 cents are added.
    """
    starting_distance: int = OrderConstants.STARTING_DISTANCE
    starting_fee: int = OrderConstants.DISTANCE_STARTING_FEE
    half_km_fee: int = OrderConstants.DISTANCE_HALF_KM_FEE

    if distance <= starting_distance:
        return starting_fee

    additional_distance: int = distance - starting_distance
    half_kms_started: int = math.ceil(additional_distance / 500)
    additional_surcharge: int = half_kms_started * half_km_fee

    return starting_fee + additional_surcharge


def items_surcharge(items: int) -> int:
    """
    Calculate the surcharge and bulk fee based on the number of items.

    Args:
        items (int): The number of items in the order.

    Returns:
        int: The total surcharge and bulk fee amount in cents.

    - No surcharge for 4 or fewer items.
    - 50 cents surcharge for each item above 4.
    - Additional 120 cents bulk fee for orders with more than 12 items.
    """
    fee: int = 0
    if items > OrderConstants.MAX_ITEMS_NO_SURCHARGE:
        additional_items: int = items - OrderConstants.MAX_ITEMS_NO_SURCHARGE
        fee = additional_items * OrderConstants.ADDITIONAL_FEE_PER_ITEM

    if items > OrderConstants.MAX_ITEMS_NO_BULK_FEE:
        fee += OrderConstants.ITEMS_BULK_FEE
    return fee


def is_rush_hour(time: str) -> bool:
    """
    Determine whether or not the order was placed during rush hour (Friday 3-7PM UTC),
    timezone offset considered. Exception should never be raised, since the field has
    been validated, but we don't want to add a rush hour fee if anything unexpected happens.
    """
    FRIDAY: int = 4
    RUSH_HOUR_START: int = 15
    RUSH_HOUR_END: int = 19

    try:
        order_time: datetime = parser.isoparse(time)
        order_time_utc = order_time.astimezone(timezone.utc)

        is_friday = order_time_utc.weekday() == FRIDAY
        is_rush_hour = RUSH_HOUR_START <= order_time_utc.hour < RUSH_HOUR_END

        return is_friday and is_rush_hour
    except Exception:
        return False
