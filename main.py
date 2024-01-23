from fastapi import FastAPI, Depends, HTTPException, Body
from pydantic import BaseModel
from datetime import datetime
import re
import math
from error_messages import (
    INVALID_CART_VALUE,
    INVALID_DELIVERY_DISTANCE,
    INVALID_NUMBER_OF_ITEMS,
    INVALID_TIME_FORMAT,
)

app = FastAPI(title="Delivery Fee API")

# Constants
MAX_DELIVERY_FEE = 1500
FREE_DELIVERY_CART_VALUE = 20000
NO_SURCHARGE_MIN_CART_VALUE = 1000
RUSH_HOUR_MULTIPLIER = 1.2
# Distance constants
STARTING_DISTANCE = 1000
DISTANCE_STARTING_FEE = 200
DISTANCE_HALF_KM_FEE = 100
# Items constants
MAX_ITEMS_NO_SURCHARGE = 4
ADDITIONAL_FEE_PER_ITEM = 50
MAX_ITEMS_NO_BULK_FEE = 12
ITEMS_BULK_FEE = 120
# Order format constants
MIN_CART_VALUE = 1
MIN_DELIVERY_DISTANCE = 0
MIN_NUMBER_OF_ITEMS = 1
TIME_FORMAT_REGEX = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
TIME_FORMAT_DATETIME = "%Y-%m-%dT%H:%M:%SZ"


# Class representing an order, the request body must follow this format.
# By default, extra fields are not forbidden, but disregarded.
class Order(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str


# Validates that the request body is correctly formatted, and returns (an)
# appropriate error description(s) where applicable.
def validate_order_data(order_data: Order = Body(...)):
    error_messages = []
    if order_data.cart_value < MIN_CART_VALUE:
        error_messages.append(INVALID_CART_VALUE)
    if order_data.delivery_distance < MIN_DELIVERY_DISTANCE:
        error_messages.append(INVALID_DELIVERY_DISTANCE)
    if order_data.number_of_items < MIN_NUMBER_OF_ITEMS:
        error_messages.append(INVALID_NUMBER_OF_ITEMS)
    if not re.match(TIME_FORMAT_REGEX, order_data.time):
        error_messages.append(INVALID_TIME_FORMAT)
    if error_messages:
        raise HTTPException(status_code=400, detail=", ".join(error_messages))
    return order_data


# Calculates the surcharge depending on the distance of the order.
def distance_surcharge(distance: int) -> int:
    if distance <= STARTING_DISTANCE:
        return DISTANCE_STARTING_FEE
    half_kms_started = math.ceil((distance - STARTING_DISTANCE) / 500)
    return DISTANCE_STARTING_FEE + (DISTANCE_HALF_KM_FEE * half_kms_started)


# Calculates the possible surcharge and bulk fee depending on the number of items.
def items_surcharge(items: int) -> int:
    fee = 0
    if items > MAX_ITEMS_NO_SURCHARGE:
        fee = ADDITIONAL_FEE_PER_ITEM * (items - MAX_ITEMS_NO_SURCHARGE)
    if items > MAX_ITEMS_NO_BULK_FEE:
        fee += ITEMS_BULK_FEE
    return fee


# Returns true if the order was placed during rush hour (Friday 3-7 PM).
def is_rush_hour(time: str) -> bool:
    try:
        order_time = datetime.strptime(time, TIME_FORMAT_DATETIME)
        if order_time.weekday() == 4:
            return 15 <= order_time.hour < 19
        else:
            return False
    # This should never happen.
    except Exception:
        return False


# Calculates the full delivery fee according to the instructions.
def calculate_delivery_fee(order_data: Order) -> float:
    fee: float = 0
    # Free delivery on orders over a certain value.
    if order_data.cart_value >= FREE_DELIVERY_CART_VALUE:
        return 0
    if order_data.cart_value < NO_SURCHARGE_MIN_CART_VALUE:
        fee = NO_SURCHARGE_MIN_CART_VALUE - order_data.cart_value
    fee += distance_surcharge(order_data.delivery_distance)
    fee += items_surcharge(order_data.number_of_items)
    if is_rush_hour(order_data.time):
        fee = fee * RUSH_HOUR_MULTIPLIER
    # The delivery fee cannot exceed this.
    if fee > MAX_DELIVERY_FEE:
        return MAX_DELIVERY_FEE
    return fee


@app.post("/delivery_fee")
def fee_calculator(order_data: Order = Depends(validate_order_data)):
    fee: int = int(calculate_delivery_fee(order_data))
    return {"delivery_fee": fee}
