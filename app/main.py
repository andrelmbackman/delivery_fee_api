from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, constr
#from datetime import datetime
#import json, jsonschema

app = FastAPI(title="Delivery Fee API")

# Constants
MIN_CART_VALUE = 1
MIN_DELIVERY_DISTANCE = 0
MIN_NUMBER_OF_ITEMS = 1
TIME_FORMAT_REGEX = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'

FREE_DELIVERY_CART_VALUE = 200000

# Class representing an order, post requests must follow this format.
class Order(BaseModel):
	cart_value: int
	delivery_distance: int
	number_of_items: int
	time: constr(regex=TIME_FORMAT_REGEX)

# Validates the data recieved in the request body.
def	validate_order_data(order_data: Order):
	error_messages = []
	if order_data.cart_value <= 0:
		error_messages.append("Cart value must be greater than 0 cents.")
	if order_data.delivery_distance < 0:
		error_messages.append("Delivery distance must not be a negative value.")
	if order_data.number_of_items <= 0:
		error_messages.append("Cart must contain at least one item.")
	if error_messages:
		raise HTTPException(status_code=400, detail=", ".join(error_messages))

@app.post("/")
def fee_calculator(order_data: Order = Depends(validate_order_data)):
	print(order_data)
	return {"recieved data": order_data}



