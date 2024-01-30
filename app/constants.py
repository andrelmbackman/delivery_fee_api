from dataclasses import dataclass


@dataclass
class OrderConstants:
    """Constants related to the full order"""

    MAX_DELIVERY_FEE: int = 1500
    FREE_DELIVERY_CART_VALUE: int = 20000
    MIN_CART_VALUE_NO_SURCHARGE: int = 1000
    RUSH_HOUR_MULTIPLIER: float = 1.2

    """Constants related to the distance surcharge"""
    STARTING_DISTANCE: int = 1000
    DISTANCE_STARTING_FEE: int = 200
    DISTANCE_HALF_KM_FEE: int = 100

    """Constants related to the items surcharge"""
    MAX_ITEMS_NO_SURCHARGE: int = 4
    ADDITIONAL_FEE_PER_ITEM: int = 50
    MAX_ITEMS_NO_BULK_FEE: int = 12
    ITEMS_BULK_FEE: int = 120


@dataclass
class ErrorMessages:
    """Error messages for raising HTTPExceptions and testing purposes"""

    INVALID_TIME_FORMAT: str = "Invalid time format: "
    INVALID_UTC_OFFSET: str = "Time string does not include timezone offset or 'Z'"
