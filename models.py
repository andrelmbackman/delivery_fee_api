from pydantic import BaseModel

# Class (model) representing an order, the request body must follow this format.
# By default, extra fields are not forbidden, but disregarded.
class Order(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str