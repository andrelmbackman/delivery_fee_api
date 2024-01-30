# Delivery Fee Calculator API

### Solution to [Wolt's engineering internship (backend) assignment](https://github.com/woltapp/engineering-internship-2024)
## Description
- The Delivery Fee Calculator API provides a single-endpoint that responds to POST requests.
- Request body format:
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

- Response: Calculated delivery fee
```json
{"delivery_fee": 710}
```
## Usage
### Using a virtual environment (Python 3.10 or higher):
#### Linux, MacOS:
```bash 
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
#### Windows:

<table>
  <tr>
    <td>
      <strong>PowerShell</strong>
    </td>
    <td>
      <strong>CMD</strong>
    </td>
  </tr>
  <tr>
  <td>

```bash
python3 -m venv .venv  
.venv/Scripts/Activate.ps1  
pip install -r requirements.txt  
uvicorn app.main:app --reload  
```

</td>
<td>

```bash
python3 -m venv .venv  
.venv/Scripts/activate.bat  
pip install -r requirements.txt  
uvicorn app.main:app --reload  
```

</td>
</tr>
</table>

#### To exit the virtual environment:
```deactivate```

## Try it out:
- Send POST requests to ```127.0.0.1:8000/delivery_fee``` or ```localhost:8000/delivery_fee```
- Access fastAPI's documentation and interact with the API: https://127.0.0.1:8000/docs
- Send a POST request from terminal:
```
curl -X "POST" -H "Content-Type: application/json" -d "{\"cart_value\": 790, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T13:00:00Z\"}" localhost:8000/delivery_fee
```
## Running the tests
<table>
  <tr>
    <th>Tests</th>
    <th>Commands</th>
  </tr>
  <tr>
    <td>All tests:</td>
    <td><code>pytest</code></td>
  </tr>
  <tr>
    <td>Unit tests:</td>
    <td><code>pytest tests/unit</code></td>
  </tr>
  <tr>
    <td>Endpoint tests:</td>
    <td><code>pytest tests/endpoint</code></td>
  </tr>
</table>

## Requirements
(No need to worry about these if you created a virtual environment)
```
fastapi==0.109.0
httpx==0.26.0
pydantic==2.5.3
pytest==7.4.4
uvicorn==0.27.0
python-dateutil==2.8.2
types-python-dateutil==2.8.19.20240106
```
#### Special thanks to [Jerry Pussinen](https://github.com/jerry-git) for the inspiring FastAPI workshop!
  
  
