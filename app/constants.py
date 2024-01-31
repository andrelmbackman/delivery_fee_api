from dataclasses import dataclass


@dataclass
class OrderConstants:
    """The delivery fee can never surpass this."""
    MAX_DELIVERY_FEE: int = 1500
    """Free delivery is granted when the chart value reaches this."""
    FREE_DELIVERY_CART_VALUE: int = 20000
    """The delivery fee is multiplied by this if the order is placed during rush hours."""
    RUSH_HOUR_MULTIPLIER: float = 1.2
    """If the cart value is less than this, the difference is added as a surcharge."""
    MIN_CART_VALUE_NO_SURCHARGE: int = 1000

    """Constants related to the distance surcharge"""
    STARTING_DISTANCE: int = 1000
    DISTANCE_STARTING_FEE: int = 200
    DISTANCE_HALF_KM_FEE: int = 100

    """Constants related to the items surcharge"""
    MAX_ITEMS_NO_SURCHARGE: int = 4
    ADDITIONAL_FEE_PER_ITEM: int = 50
    MAX_ITEMS_NO_BULK_FEE: int = 12
    ITEMS_BULK_FEE: int = 120

    """Rush hour day is 4, Friday (count starts from 0)"""
    RUSH_HOUR_DAY: int = 4
    """The starting hour: 15:00:00"""
    RUSH_HOUR_START: int = 15
    """Rush hour ends at 19:00:00"""
    RUSH_HOUR_END: int = 19

@dataclass
class ErrorMessages:
    """Error messages for raising HTTPExceptions and testing purposes"""

    INVALID_TIME_FORMAT: str = "Invalid time format: "
    INVALID_UTC_OFFSET: str = "Time string does not include timezone offset or 'Z'"
