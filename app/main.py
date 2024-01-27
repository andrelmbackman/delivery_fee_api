from fastapi import FastAPI
from datetime import datetime, timezone
from dateutil import parser
import math
from app.models import Order
import app.constants as constants

app = FastAPI(title="Delivery Fee API")


def calculate_delivery_fee(order_data: Order) -> float:
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
    fee: float = 0
    if order_data.cart_value >= constants.FREE_DELIVERY_CART_VALUE:
        return 0
    if order_data.cart_value < constants.NO_SURCHARGE_MIN_CART_VALUE:
        fee = constants.NO_SURCHARGE_MIN_CART_VALUE - order_data.cart_value
    fee += distance_surcharge(order_data.delivery_distance)
    fee += items_surcharge(order_data.number_of_items)
    if is_rush_hour(order_data.time):
        fee = fee * constants.RUSH_HOUR_MULTIPLIER
    if fee > constants.MAX_DELIVERY_FEE:
        return constants.MAX_DELIVERY_FEE
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
    if distance <= constants.STARTING_DISTANCE:
        return constants.DISTANCE_STARTING_FEE
    half_kms_started = math.ceil((distance - constants.STARTING_DISTANCE) / 500)
    return constants.DISTANCE_STARTING_FEE + (constants.DISTANCE_HALF_KM_FEE * half_kms_started)


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
    fee = 0
    if items > constants.MAX_ITEMS_NO_SURCHARGE:
        fee = constants.ADDITIONAL_FEE_PER_ITEM * (items - constants.MAX_ITEMS_NO_SURCHARGE)
    if items > constants.MAX_ITEMS_NO_BULK_FEE:
        fee += constants.ITEMS_BULK_FEE
    return fee


def is_rush_hour(time: str) -> bool:
    """
    Determine whether or not the order was placed during rush hour (Friday 3-7PM UTC),
    timezone offset considered. Exception should never be raised, since the field has
    been validated, but we don't want to add a rush hour fee if anything unexpected happens.
    """
    try:
        order_time: datetime = parser.isoparse(time)
        order_time_utc = order_time.astimezone(timezone.utc)
        return order_time_utc.weekday() == 4 and 15 <= order_time_utc.hour < 19
    except Exception:
        return False


@app.post("/delivery_fee")
def fee_calculator(order_data: Order):
    fee: int = int(calculate_delivery_fee(order_data))
    return {"delivery_fee": fee}
