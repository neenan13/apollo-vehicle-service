import os
import sys
import tempfile

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Vehicle

# --- Test DB setup ---------------------------------------------------------

# Use a temp SQLite database for tests so we don't alter vehicles.db.

db_fd, db_path = tempfile.mkstemp()
TEST_DB_URL = f"sqlite:///{db_path}"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():

    """
    Override the app's DB dependency so all requests use the test database.
    """

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def reset_db():

    """
    Clear all data between tests.
    """

    db = TestingSessionLocal()
    try:
        db.query(Vehicle).delete()
        db.commit()
    finally:
        db.close()


def teardown_module(module):

    """
    Remove the temp SQLite file when the test module is done.
    """

    os.close(db_fd)
    os.unlink(db_path)


# --- Tests -----------------------------------------------------------------


def test_create_vehicle_success():
    reset_db()
    payload = {
        "vin": "abc123",
        "manufacturer_name": "Toyota",
        "description": "Nice",
        "horse_power": 150,
        "model_name": "Corolla",
        "model_year": 2020,
        "purchase_price": 20000.50,
        "fuel_type": "Gasoline",
    }

    r = client.post("/vehicle", json=payload)
    assert r.status_code == 201
    data = r.json()

    # VIN should be normalized to uppercase

    assert data["vin"] == "ABC123"
    assert data["model_name"] == "Corolla"


def test_create_vehicle_duplicate_vin_returns_422():
    reset_db()
    payload = {
        "vin": "dupVin",
        "manufacturer_name": "Honda",
        "description": "First car",
        "horse_power": 140,
        "model_name": "Civic",
        "model_year": 2019,
        "purchase_price": 19000.00,
        "fuel_type": "Gasoline",
    }

    r1 = client.post("/vehicle", json=payload)
    assert r1.status_code == 201

    # Same VIN, different case should still be treated as duplicate.

    payload["vin"] = "DUPVIN"
    r2 = client.post("/vehicle", json=payload)
    assert r2.status_code == 422


def test_get_vehicle_not_found_returns_404():
    reset_db()
    r = client.get("/vehicle/DOESNOTEXIST")
    assert r.status_code == 404


def test_list_vehicles_returns_created_entries():
    reset_db()

    v1 = {
        "vin": "v1",
        "manufacturer_name": "Toyota",
        "description": "Car 1",
        "horse_power": 120,
        "model_name": "Yaris",
        "model_year": 2018,
        "purchase_price": 15000.0,
        "fuel_type": "Gasoline",
    }
    v2 = {
        "vin": "v2",
        "manufacturer_name": "Ford",
        "description": "Car 2",
        "horse_power": 180,
        "model_name": "Focus",
        "model_year": 2021,
        "purchase_price": 22000.0,
        "fuel_type": "Gasoline",
    }

    client.post("/vehicle", json=v1)
    client.post("/vehicle", json=v2)

    r = client.get("/vehicle")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    vins = {item["vin"] for item in data}
    assert "V1" in vins
    assert "V2" in vins


def test_update_vehicle_vin_mismatch_returns_422():
    reset_db()

    create_payload = {
        "vin": "matchvin",
        "manufacturer_name": "BMW",
        "description": "Original",
        "horse_power": 200,
        "model_name": "3 Series",
        "model_year": 2022,
        "purchase_price": 40000.0,
        "fuel_type": "Gasoline",
    }
    client.post("/vehicle", json=create_payload)

    # Situation where body VIN does not match the path VIN.

    update_payload = {
        **create_payload,
        "vin": "differentvin",
        "description": "Updated",
    }

    r = client.put("/vehicle/MATCHVIN", json=update_payload)
    assert r.status_code == 422


def test_delete_vehicle_success_and_then_404_on_get():
    reset_db()

    payload = {
        "vin": "todelete",
        "manufacturer_name": "Mazda",
        "description": "Delete me",
        "horse_power": 155,
        "model_name": "3",
        "model_year": 2017,
        "purchase_price": 16000.0,
        "fuel_type": "Gasoline",
    }
    client.post("/vehicle", json=payload)

    r_del = client.delete("/vehicle/TODELETE")
    assert r_del.status_code == 204

    # Once deleted, we expect the GET to return 404.


    r_get = client.get("/vehicle/TODELETE")
    assert r_get.status_code == 404


def test_delete_vehicle_not_found_returns_404():
    reset_db()
    r = client.delete("/vehicle/NOSUCHVIN")
    assert r.status_code == 404
