from fastapi import FastAPI, Depends
from datetime import datetime, timezone
from dateutil import parser
import math
from app.models import Order
from app.validation import validate_order_data
import app.constants as const

app = FastAPI(title="Delivery Fee API")


def calculate_delivery_fee(order_data: Order) -> float:
    """
    Calculate the full delivery fee of the order.
    """
    fee: float = 0
    if order_data.cart_value >= const.FREE_DELIVERY_CART_VALUE:
        return 0
    if order_data.cart_value < const.NO_SURCHARGE_MIN_CART_VALUE:
        fee = const.NO_SURCHARGE_MIN_CART_VALUE - order_data.cart_value
    fee += distance_surcharge(order_data.delivery_distance)
    fee += items_surcharge(order_data.number_of_items)
    if is_rush_hour(order_data.time):
        fee = fee * const.RUSH_HOUR_MULTIPLIER
    if fee > const.MAX_DELIVERY_FEE:  # The delivery fee cannot exceed this.
        return const.MAX_DELIVERY_FEE
    return fee


def distance_surcharge(distance: int) -> int:
    """
    Calculate the surcharge depending on the delivery distance of the order.
    """
    if distance <= const.STARTING_DISTANCE:
        return const.DISTANCE_STARTING_FEE
    half_kms_started = math.ceil((distance - const.STARTING_DISTANCE) / 500)
    return const.DISTANCE_STARTING_FEE + (const.DISTANCE_HALF_KM_FEE * half_kms_started)


def items_surcharge(items: int) -> int:
    """
    Calculate the possible surcharge and bulk fee depending on the number of items.
    """
    fee = 0
    if items > const.MAX_ITEMS_NO_SURCHARGE:
        fee = const.ADDITIONAL_FEE_PER_ITEM * (items - const.MAX_ITEMS_NO_SURCHARGE)
    if items > const.MAX_ITEMS_NO_BULK_FEE:
        fee += const.ITEMS_BULK_FEE
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
def fee_calculator(order_data: Order = Depends(validate_order_data)):
    fee: int = int(calculate_delivery_fee(order_data))
    return {"delivery_fee": fee}
