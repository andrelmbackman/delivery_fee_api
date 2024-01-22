from fastapi.testclient import TestClient
from app.main import app

def test_empty_request_body():
	with TestClient(app) as client:
		response = client.post("/")
	assert response.status_code == 422

def test_invalid_date():
	with TestClient(app) as client:
		data = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "0-01-15T13:00:00"
		}
		response = client.post("/", json=data)
	assert response.status_code == 400

def test_valid_request():
	with TestClient(app) as client:
		data = {
			"cart_value": 790,
			"delivery_distance": 2235,
			"number_of_items": 4,
			"time": "2024-01-15T13:00:00Z"
		}
		expected_response = {"delivery_fee": 710}
		response = client.post("/", json=data)
	assert response.status_code == 200
	assert response.json() == expected_response
