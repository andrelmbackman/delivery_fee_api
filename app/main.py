from fastapi import FastAPI
from app.models import Order, DeliveryFeeResponse
from app.delivery_fee import calculate_delivery_fee


app = FastAPI(title="Delivery Fee API")


@app.post("/delivery_fee")
def fee_calculator(order_data: Order) -> DeliveryFeeResponse:
    fee: int = calculate_delivery_fee(order_data)
    return DeliveryFeeResponse(delivery_fee=fee)
