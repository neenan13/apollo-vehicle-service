# Apollo Vehicle Service

A RESTful web service providing CRUD operations for vehicle management, built with FastAPI and SQLAlchemy.

## Features

- Full CRUD API for vehicle records
- Case-insensitive VIN handling (automatically normalized to uppercase)
- Input validation with detailed error messages
- SQLite database for simplicity and portability
- Comprehensive testing
- RESTful design following HTTP standards

## Requirements

- Python 3.10 or higher
- pip package manager

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # (On Windows: venv\Scripts\activate)
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
.
├── app/
│   ├── __init__.py 
│   ├── main.py
│   ├── database.py 
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_vehicle.py
├── reset_db.py
├── run.sh
├── requirements.txt
└── README.md
```

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database** (creates empty DB, not required)
   ```bash
   python reset_db.py
   ```

3. **Start the server**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
   Or directly:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Interactive API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`



### Create a Vehicle
```bash
curl -X POST http://localhost:8000/vehicle \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "1HGBH41JXMN109186",
    "manufacturer_name": "Toyota",
    "description": "Reliable family sedan",
    "horse_power": 203,
    "model_name": "Camry",
    "model_year": 2020,
    "purchase_price": 24999.99,
    "fuel_type": "Gasoline"
  }'
```

**Response (201 Created):**
```json
{
  "vin": "1HGBH41JXMN109186",
  "manufacturer_name": "Toyota",
  "description": "Reliable family sedan",
  "horse_power": 203,
  "model_name": "Camry",
  "model_year": 2020,
  "purchase_price": 24999.99,
  "fuel_type": "Gasoline"
}
```

### Get All Vehicles
```bash
curl http://localhost:8000/vehicle
```

**Response (200 OK):**
```json
[
  {
    "vin": "1HGBH41JXMN109186",
    "manufacturer_name": "Toyota",
    "description": "Reliable family sedan",
    "horse_power": 203,
    "model_name": "Camry",
    "model_year": 2020,
    "purchase_price": 24999.99,
    "fuel_type": "Gasoline"
  }
]
```

### Get Vehicle by VIN
```bash
curl http://localhost:8000/vehicle/1HGBH41JXMN109186
```

**Response (200 OK):**
```json
{
  "vin": "1HGBH41JXMN109186",
  "manufacturer_name": "Toyota",
  "description": "Reliable family sedan",
  "horse_power": 203,
  "model_name": "Camry",
  "model_year": 2020,
  "purchase_price": 24999.99,
  "fuel_type": "Gasoline"
}
```

### Update a Vehicle
```bash
curl -X PUT http://localhost:8000/vehicle/1HGBH41JXMN109186 \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "1HGBH41JXMN109186",
    "manufacturer_name": "Toyota",
    "description": "Updated: Excellent condition",
    "horse_power": 203,
    "model_name": "Camry",
    "model_year": 2020,
    "purchase_price": 23999.99,
    "fuel_type": "Gasoline"
  }'
```

**Response (200 OK):**
```json
{
  "vin": "1HGBH41JXMN109186",
  "manufacturer_name": "Toyota",
  "description": "Updated: Excellent condition",
  "horse_power": 203,
  "model_name": "Camry",
  "model_year": 2020,
  "purchase_price": 23999.99,
  "fuel_type": "Gasoline"
}
```

### Delete a Vehicle
```bash
curl -X DELETE http://localhost:8000/vehicle/1HGBH41JXMN109186
```

**Response (204 No Content):**
(Empty response body)

### Error Examples

**Duplicate VIN (422):**
```bash

# Trying to create a vehicle with existing VIN

curl -X POST http://localhost:8000/vehicle \
  -H "Content-Type: application/json" \
  -d '{"vin": "1HGBH41JXMN109186", ...}'
```

**Response:**
```json
{
  "detail": "VIN already exists"
}
```

**Invalid Data (422):**
```bash
curl -X POST http://localhost:8000/vehicle \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "TEST123",
    "manufacturer_name": "Honda",
    "horse_power": -100,
    "model_name": "Civic",
    "model_year": 2020,
    "purchase_price": 20000,
    "fuel_type": "Gasoline"
  }'
```

**Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "horse_power"],
      "msg": "horse_power must be positive",
      "type": "value_error"
    }
  ]
}
```

**Vehicle Not Found (404):**
```bash
curl http://localhost:8000/vehicle/NONEXISTENT
```

**Response:**
```json
{
  "detail": "Vehicle not found"
}
```

## API Endpoints

### 1. List All Vehicles
```
GET /vehicle
```
**Response:** `200 OK` with JSON array of all vehicles

### 2. Create Vehicle
```
POST /vehicle
Content-Type: application/json

{
  "vin": "1HGBH41JXMN109186",
  "manufacturer_name": "Toyota",
  "description": "Reliable sedan",
  "horse_power": 150,
  "model_name": "Camry",
  "model_year": 2020,
  "purchase_price": 24000.50,
  "fuel_type": "Gasoline"
}
```
**Response:** `201 Created` with the created vehicle (VIN normalized to uppercase)

### 3. Get Vehicle by VIN
```
GET /vehicle/{vin}
```
**Response:** `200 OK` with vehicle details, or `404 Not Found`

### 4. Update Vehicle
```
PUT /vehicle/{vin}
Content-Type: application/json

{
  "vin": "1HGBH41JXMN109186",
  "manufacturer_name": "Toyota",
  "description": "Updated description",
  "horse_power": 160,
  "model_name": "Camry",
  "model_year": 2020,
  "purchase_price": 23000.00,
  "fuel_type": "Gasoline"
}
```
**Response:** `200 OK` with updated vehicle
**Note:** VIN in path and body must match (case-insensitive)

### 5. Delete Vehicle
```
DELETE /vehicle/{vin}
```
**Response:** `204 No Content` on success, or `404 Not Found`

## Error Handling

- **400 Bad Request**: Malformed JSON in request body
- **404 Not Found**: Vehicle with specified VIN doesn't exist
- **422 Unprocessable Entity**: Valid JSON but invalid data (such as validation errors, duplicate VIN, VIN mismatch)


## Data Validation

The service validates:
- **VIN**: Required, automatically converted to uppercase for case-insensitive uniqueness
- **Horse Power**: Must be positive integer
- **Model Year**: Must be between 1886 and 2100 (inclusive)
- **Purchase Price**: Must be positive
- **Manufacturer Name, Model Name, Fuel Type**: Required strings
- **Description**: Optional string

## Running Tests

The test suite uses pytest and covers all CRUD operations plus edge cases.

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app
```

### Test Coverage
- Create vehicle with valid data
- Duplicate VIN detection, case insensitive
- List all vehicles
- Get vehicle by VIN
- Update vehicle with VIN mismatch detection
- Delete vehicle

## Database

The application uses SQLite with a file-based database (`vehicles.db`) created automatically on first run.

### Reset Database
To clear all data and start fresh:
```bash
python reset_db.py
```

### Database Schema
```sql
CREATE TABLE vehicles (
    vin TEXT PRIMARY KEY,
    manufacturer_name TEXT NOT NULL,
    description TEXT,
    horse_power INTEGER NOT NULL,
    model_name TEXT NOT NULL,
    model_year INTEGER NOT NULL,
    purchase_price REAL NOT NULL,
    fuel_type TEXT NOT NULL
);
```

## Development Notes

### VIN Handling
- VINs are stored in uppercase in the database
- All VIN comparisons are case-insensitive
- Input VINs are automatically normalized to uppercase

### Adding New Fields
To add a new field to the Vehicle model:
1. Update `app/models.py` (add SQLAlchemy Column)
2. Update `app/schemas.py` (add to VehicleBase)
3. Create database migration or reset database
4. Update tests as needed

### Dependencies
- **FastAPI**: Modern web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type hints
- **Uvicorn**: ASGI server
- **Pytest**: Testing framework

## Future Enhancements

- [ ] Add filtering and search capabilities
- [ ] Add authentication/authorization
- [ ] Implement caching layer
- [ ] Add logging and monitoring
- [ ] Deploy to cloud platform


## Contact

Neena Naikar