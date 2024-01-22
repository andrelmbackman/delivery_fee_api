from fastapi.testclient import TestClient
from app.main import app

API_ENDPOINT = "/delivery_fee"

def test_invalid_request_body():
	with TestClient(app) as client:
		response = client.post(API_ENDPOINT) #empty request body
		assert response.status_code == 422
		data = {
			"cart_value": 790,
			"delivery_distance": 2235
		}
		response = client.post(API_ENDPOINT, json=data) #invalid request body
		assert response.status_code == 422
		data = {
			"value": 790,
			"distance": 2235,
			"items": 4,
			"time": "2024-01-15T13:00:00Z",
		}
		response = client.post(API_ENDPOINT, json=data) #invalid request body
		assert response.status_code == 422

def test_invalid_distance():
	with TestClient(app) as client:
		data = {
			"cart_value": 790,
			"delivery_distance": -2235,
			"number_of_items": 4,
			"time": "2020-0-15Ö00:00:00Q"
		}
		response = client.post(API_ENDPOINT, json=data)
		assert response.status_code == 400
		assert "Delivery distance must not be a negative value" in response.json()["detail"]

def test_invalid_time_formats():
	with TestClient(app) as client:
		data = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "2020-0-15Ö00:00:00Q"
		}
		response = client.post(API_ENDPOINT, json=data)
		assert response.status_code == 400
		assert "Invalid time format" in response.json()["detail"]
		data = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "0-01-15T13:00:00"
		}
		response = client.post(API_ENDPOINT, json=data)
		assert response.status_code == 400
		assert "Invalid time format" in response.json()["detail"]
		data = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "2023-x-y5T13:00:00"
		}
		response = client.post(API_ENDPOINT, json=data)
		assert response.status_code == 400
		assert "Invalid time format" in response.json()["detail"]

def test_valid_request():
	with TestClient(app) as client:
		data = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "2024-01-15T13:00:00Z"
		}
		expected_response = {"delivery_fee": 710}
		response = client.post(API_ENDPOINT, json=data)
	assert response.status_code == 200
	assert response.json() == expected_response

def test_rush_hour():
	with TestClient(app) as client:
		data = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "2024-01-26T16:00:00Z"
		}
		expected_response = {"delivery_fee": 852}
		response = client.post(API_ENDPOINT, json=data)
	assert response.status_code == 200
	assert response.json() == expected_response

def test_valid_cheap_order():
	with TestClient(app) as client:
		data = {
			"cart_value": 1000,
			"delivery_distance": 999,
			"number_of_items": 4,
			"time": "2024-01-15T13:00:00Z"
		}
		expected_response = {"delivery_fee": 200}
		response = client.post(API_ENDPOINT, json=data)
	assert response.status_code == 200
	assert response.json() == expected_response

def test_free_delivery():
	with TestClient(app) as client:
		data = {
			"cart_value": 999999,
			"delivery_distance": 500,
			"number_of_items": 1,
			"time": "2024-01-15T13:00:00Z"
		}
		expected_response = {"delivery_fee": 0}
		response = client.post(API_ENDPOINT, json=data)
		assert response.status_code == 200
		assert response.json() == expected_response

def test_max_delivery_fee():
	with TestClient(app) as client:
		data = {
			"cart_value": 100,
			"delivery_distance": 50000,
			"number_of_items": 100,
			"time": "2024-01-15T13:00:00Z"
		}
		expected_response = {"delivery_fee": 1500}
		response = client.post(API_ENDPOINT, json=data)
		assert response.status_code == 200
		assert response.json() == expected_response