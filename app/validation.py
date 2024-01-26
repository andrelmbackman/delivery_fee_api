from fastapi import HTTPException, Body
from dateutil import parser
from app.models import Order
import app.error_messages as err


def validate_order_data(order_data: Order = Body(...)) -> Order:
    """
    Validate that the request body is correctly formatted, and raise an
    HTTPException where applicable.
    """
    error_messages = []
    try:
        validate_iso_time_string(order_data.time)
    except Exception as e:
        error_messages.append(str(e))
    if error_messages:
        raise HTTPException(status_code=400, detail=", ".join(error_messages))
    return order_data


def validate_iso_time_string(time_string: str):
    """
    Validate that the time string fits the ISO 8061 standard.
    """
    try:
        parsed_time = parser.isoparse(time_string)
        if parsed_time.tzinfo is None and time_string[-1] != "Z":
            raise ValueError(err.INVALID_UTC_OFFSET)
    except Exception as e:
        raise ValueError(err.INVALID_TIME_FORMAT + str(e))
