from fastapi import FastAPI, Depends, HTTPException, Body
from datetime import datetime, timezone
from dateutil import parser
import math
from app.models import Order
import app.constants as const
import app.error_messages as err

app = FastAPI(title="Delivery Fee API")


# Calculates the full delivery fee according to the instructions.
def calculate_delivery_fee(order_data: Order) -> float:
    fee: float = 0
    # Free delivery on orders over a certain value.
    if order_data.cart_value >= const.FREE_DELIVERY_CART_VALUE:
        return 0
    if order_data.cart_value < const.NO_SURCHARGE_MIN_CART_VALUE:
        fee = const.NO_SURCHARGE_MIN_CART_VALUE - order_data.cart_value
    fee += distance_surcharge(order_data.delivery_distance)
    fee += items_surcharge(order_data.number_of_items)
    if is_rush_hour(order_data.time):
        fee = fee * const.RUSH_HOUR_MULTIPLIER
    # The delivery fee cannot exceed this.
    if fee > const.MAX_DELIVERY_FEE:
        return const.MAX_DELIVERY_FEE
    return fee


# Calculates the surcharge depending on the distance of the order.
def distance_surcharge(distance: int) -> int:
    if distance <= const.STARTING_DISTANCE:
        return const.DISTANCE_STARTING_FEE
    half_kms_started = math.ceil((distance - const.STARTING_DISTANCE) / 500)
    return const.DISTANCE_STARTING_FEE + (const.DISTANCE_HALF_KM_FEE * half_kms_started)


# Calculates the possible surcharge and bulk fee depending on the number of items.
def items_surcharge(items: int) -> int:
    fee = 0
    if items > const.MAX_ITEMS_NO_SURCHARGE:
        fee = const.ADDITIONAL_FEE_PER_ITEM * (items - const.MAX_ITEMS_NO_SURCHARGE)
    if items > const.MAX_ITEMS_NO_BULK_FEE:
        fee += const.ITEMS_BULK_FEE
    return fee


# Returns true if the order was placed during rush hour (Friday 3-7 PM) UTC.
def is_rush_hour(time: str) -> bool:
    try:
        order_time: datetime = parser.isoparse(time)
        print(order_time)
        order_time_utc = order_time.astimezone(timezone.utc)
        return order_time_utc.weekday() == 4 and 15 <= order_time_utc.hour < 19
    # This should never happen, parsed in validate_order_data
    except Exception:
        print("DOES NOT COMPUTE DATETIME")
        return False


# Validates that the request body is correctly formatted, and returns (an)
# appropriate error description(s) where applicable.
def validate_order_data(order_data: Order = Body(...)):
    error_messages = []
    if order_data.cart_value < const.MIN_CART_VALUE:
        error_messages.append(err.INVALID_CART_VALUE)
    if order_data.delivery_distance < const.MIN_DELIVERY_DISTANCE:
        error_messages.append(err.INVALID_DELIVERY_DISTANCE)
    if order_data.number_of_items < const.MIN_NUMBER_OF_ITEMS:
        error_messages.append(err.INVALID_NUMBER_OF_ITEMS)
    try:
        print(parser.isoparse(order_data.time))
        parser.isoparse(order_data.time)
    except Exception as e:
        error_messages.append(err.INVALID_TIME_FORMAT + str(e))
    if error_messages:
        raise HTTPException(status_code=400, detail=", ".join(error_messages))
    return order_data


@app.post("/delivery_fee")
def fee_calculator(order_data: Order = Depends(validate_order_data)):
    fee: int = int(calculate_delivery_fee(order_data))
    return {"delivery_fee": fee}
