# Delivery Fee Calculator API

### This is my solution to [Wolt's engineering internship (backend) assignment](https://github.com/woltapp/engineering-internship-2024)
## Description
- The delivery fee calculator is a single-endpoint API that responds to POST-requests.
- The request body should look like:
```json
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```
##### Field details

| Field             | Type  | Description                                                               | Example value                             |
|:---               |:---   |:---                                                                       |:---                                       |
|cart_value         |Integer|Value of the shopping cart __in cents__.                                   |__790__ (790 cents = 7.90€)                |
|delivery_distance  |Integer|The distance between the store and customer’s location __in meters__.      |__2235__ (2235 meters = 2.235 km)          |
|number_of_items    |Integer|The __number of items__ in the customer's shopping cart.                   |__4__ (customer has 4 items in the cart)   |
|time               |String |Order time in UTC in [ISO format](https://en.wikipedia.org/wiki/ISO_8601). |__2024-01-15T13:00:00Z__                   |

- The response will be the calculated delivery fee:
```json
{"delivery_fee": 710}
```
## Usage
### The simplest way is using a virtual environment (python 3.10 or higher):
#### Linux, MacOS:
```bash 
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
#### Windows:
- same, but replace ```source .venv/bin/activate```  
with ```.venv/Scripts/Activate.ps1``` (PowerShell)
or ```.venv/Scripts/activate.bat``` (CMD)

#### To exit the virtual environment:
```deactivate```

## Try it out:
- send post requests to ```127.0.0.1:8000/delivery_fee``` 
- alternative address: ```localhost:8000/delivery_fee```
- in a browser: https://127.0.0.1:8000/docs shows fastAPI's documentation and lets you try it out
- send a post request from terminal:
```
curl -X "POST" -H "Content-Type: application/json" -d "{\"cart_value\": 790, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T13:00:00Z\"}" localhost:8000/delivery_fee
```
### to run the tests:
```pytest```
- The test cases can be found in /tests/delivery_fee_tests.py
## Requirements
(No need to worry about these if you created a virtual environment)
```
fastapi==0.109.0
httpx==0.26.0
pydantic==2.5.3
pytest==7.4.4
uvicorn==0.27.0
python-dateutil==2.8.2
```
#### Special thanks to [Jerry Pussinen](https://github.com/jerry-git) for the inspiring FastAPI workshop!
  
  
