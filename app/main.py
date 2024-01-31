from fastapi import FastAPI
from app.models import Order, DeliveryFeeResponse
from app.delivery_fee import calculate_delivery_fee


app = FastAPI(title="Delivery Fee API")


@app.post("/delivery_fee")
def fee_calculator(order_data: Order) -> DeliveryFeeResponse:
    """Calculate the delivery fee based on the provided order data.

    Args:
        order_data (Order): The order details including cart value, delivery distance, number of items, and order time.

    Returns:
        DeliveryFeeResponse: An object containing the calculated delivery fee in cents.

    Description:
    This endpoint calculates the delivery fee for an order based on the provided order data.
    The fee is computed using the calculate_delivery_fee function from delivery_fee.py.
    The calculated fee is then returned as part of a DeliveryFeeResponse object.

    Example:
        {
            "cart_value": 975,
            "delivery_distance": 3520,
            "number_of_items": 3,
            "time": "2024-01-31T17:00:00Z"
        }
    """
    fee: int = calculate_delivery_fee(order_data)
    return DeliveryFeeResponse(delivery_fee=fee)
