from fastapi import HTTPException
from pydantic import BaseModel, PositiveInt, NonNegativeInt, field_validator
from dateutil import parser
from app.error_messages import INVALID_TIME_FORMAT, INVALID_UTC_OFFSET

class Order(BaseModel):
    """
    Class (model) representing an order, the request body must follow this format.
    By default, extra fields are not forbidden, but disregarded. Pydantic handles the
    input validation by utilizing PositiveInt and NonNegativeInt data types.
    Model utilizes field_validator to ensure that the value is not a coerced string.
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
            raise ValueError("Value must be a positive integer, not a string")
        return value

    @field_validator("time")
    @classmethod
    def validate_iso_time_string(cls, time):
        """Validate that the time string fits the ISO 8061 standard."""
        try:
            parsed_time = parser.isoparse(time)
            if parsed_time.tzinfo is None and time[-1] != "Z":
                raise HTTPException(status_code=400, detail=INVALID_UTC_OFFSET)
        except Exception as e:
            raise HTTPException(status_code=400, detail=(INVALID_TIME_FORMAT + str(e)))
        return time
