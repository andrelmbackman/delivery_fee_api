from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, Field
from dateutil import parser
from app.constants import ErrorMessages


"""Error messages for raising HTTPException when receiving incorrect time formats."""
invalid_utc_err: str = ErrorMessages.INVALID_UTC_OFFSET
invalid_time_err: str = ErrorMessages.INVALID_TIME_FORMAT


class Order(BaseModel):
    """
    Class (model) representing an order, the request body must follow this format.
    By default, extra fields are not forbidden, but disregarded. Pydantic handles the
    input validation by utilizing PositiveInt and NonNegativeInt data types.
    Model utilizes field_validator to ensure that the value is not a coerced string.

    Attributes:
        cart_value (int): The value of the shopping cart in cents.
        delivery_distance (int): The distance between the store and customer's location in meters.
        number_of_items (int): The number of items in the customer's shopping cart.
        time (str): Order time in ISO format.
    """

    cart_value: int = Field(strict=True, ge=0)
    delivery_distance: int = Field(strict=True, ge=0)
    number_of_items: int = Field(strict=True, ge=1)
    time: str

    @field_validator("time")
    @classmethod
    def validate_iso_time_string(cls, time):
        """Validate that the time string fits the ISO 8061 standard."""
        try:
            parsed_time = parser.isoparse(time)
            if parsed_time.tzinfo is None and time[-1] != "Z":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=invalid_utc_err
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(invalid_time_err + str(e)),
            )
        return time


class DeliveryFeeResponse(BaseModel):
    """Model representing the response body."""

    delivery_fee: int = Field(strict=True, ge=0)
