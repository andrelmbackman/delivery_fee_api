from pydantic import BaseModel, PositiveInt, NonNegativeInt, field_validator

"""
Class (model) representing an order, the request body must follow this format.
By default, extra fields are not forbidden, but disregarded. Pydantic handles the
input validation by utilizing PositiveInt and NonNegativeInt data types.
Model utilizes field_validator to ensure that the value is not a coerced string.
"""


class Order(BaseModel):
    cart_value: PositiveInt
    delivery_distance: NonNegativeInt
    number_of_items: PositiveInt
    time: str

    @field_validator(
        "cart_value", "delivery_distance", "number_of_items", mode="before"
    )
    def validate_not_string(cls, value):
        if isinstance(value, str):
            raise ValueError("Value must be a positive integer, not a string")
        return value
