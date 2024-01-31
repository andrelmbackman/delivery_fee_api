from datetime import datetime, timezone
from dateutil import parser
import math
from app.models import Order
from app.constants import OrderConstants


def calculate_delivery_fee(order_data: Order) -> int:
    """Calculate the full delivery fee of the order.

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

    fee += cart_value_surcharge(order_data.cart_value)
    fee += distance_surcharge(order_data.delivery_distance)
    fee += items_surcharge(order_data.number_of_items)

    if is_rush_hour(order_data.time):
        multiplied_fee: float = fee * OrderConstants.RUSH_HOUR_MULTIPLIER
        fee = round(multiplied_fee)

    if fee > OrderConstants.MAX_DELIVERY_FEE:
        return OrderConstants.MAX_DELIVERY_FEE

    return fee


def cart_value_surcharge(chart_value: int) -> int:
    """Return 0 if the chart_value is higher or equal to 1000 (10€),
    otherwise return the difference so they add up to 1000.
    """
    min_chart_value: int = OrderConstants.MIN_CART_VALUE_NO_SURCHARGE
    return max(0, min_chart_value - chart_value)


def distance_surcharge(distance: int) -> int:
    """Calculate the delivery surcharge based on the given distance (in meters).

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
    """Calculate the surcharge and bulk fee based on the number of items.

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
    """Determines whether an order was placed during rush hour (Friday 3-7 PM UTC).

    Args:
        time (str): The ISO 8601 formatted time string representing the order placement time.

    Returns:
        bool: True if the order was placed during rush hour, False otherwise.

    Note:
        The rush hour is defined as Friday between 3:00 PM (inclusive) and 7:00 PM (exclusive) in UTC.
        The timezone offset is considered during the evaluation.
        No exceptions should be raised during the execution, as the input is assumed to be validated.
        If any unexpected error occurs, the function returns False to avoid applying a rush hour fee incorrectly.
    """
    rush_day: int = OrderConstants.RUSH_HOUR_DAY
    rush_start: int = OrderConstants.RUSH_HOUR_START
    rush_end: int = OrderConstants.RUSH_HOUR_END

    try:
        order_time: datetime = parser.isoparse(time)
        order_time_utc = order_time.astimezone(timezone.utc)

        is_friday = order_time_utc.weekday() == rush_day
        is_rush_hour = rush_start <= order_time_utc.hour < rush_end

        return is_friday and is_rush_hour
    except Exception:
        return False
