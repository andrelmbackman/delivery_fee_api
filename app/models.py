from fastapi import HTTPException
from pydantic import BaseModel, PositiveInt, NonNegativeInt, field_validator
from dateutil import parser
import app.error_messages as error_messages

class Order(BaseModel):
    """
    Class (model) representing an order, the request body must follow this format.
    By default, extra fields are not forbidden, but disregarded. Pydantic handles the
    input validation by utilizing PositiveInt and NonNegativeInt data types.
    Model utilizes field_validator to ensure that the value is not a coerced string.

    Attributes:
        cart_value (NonNegativeInt): The value of the shopping cart in cents.
        delivery_distance (NonNegativeInt): The distance between the store and customer's location in meters.
        number_of_items (PositiveInt): The number of items in the customer's shopping cart.
        time (str): Order time in ISO format.
    """
    cart_value: NonNegativeInt
    delivery_distance: NonNegativeInt
    number_of_items: PositiveInt
    time: str

    @field_validator(
        "cart_value", "delivery_distance", "number_of_items", mode="before"
    )
    @classmethod
    def validate_not_string(cls, value):
        if isinstance(value, str):
            raise HTTPException(status_code=400, detail=error_messages.INT_NOT_STRING)
        return value

    @field_validator("time")
    @classmethod
    def validate_iso_time_string(cls, time):
        """Validate that the time string fits the ISO 8061 standard."""
        try:
            parsed_time = parser.isoparse(time)
            if parsed_time.tzinfo is None and time[-1] != "Z":
                raise HTTPException(status_code=400, detail=error_messages.INVALID_UTC_OFFSET)
        except Exception as e:
            raise HTTPException(status_code=400, detail=(error_messages.INVALID_TIME_FORMAT + str(e)))
        return time
