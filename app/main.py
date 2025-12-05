from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleResponse

# Create tables on startup

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Apollo Vehicle Service")


# 400 and 422 Error Handling

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
   
    """
    Distinguish malformed JSON (error 400) from valid JSON with invalid fields (error 422.)
    FastAPI/Pydantic groups both under RequestValidationError.
    """

    if exc.body is None:
        return JSONResponse(status_code=400, content={"detail": exc.errors()})
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


# -------------------------------
# CRUD
# -------------------------------

@app.get("/vehicle", response_model=list[VehicleSchema])
def list_vehicles(db: Session = Depends(get_db)):

    """Return all vehicles."""

    return db.query(Vehicle).all()


@app.post("/vehicle", response_model=VehicleResponse, status_code=201)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
   
    """
    Creates a new vehicle, ensuring a unique VIN.
    """

    vin = payload.vin.upper()
    if db.query(Vehicle).filter(Vehicle.vin == vin).first():
        raise HTTPException(status_code=422, detail="VIN already exists")

    vehicle = Vehicle(**payload.dict())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


@app.get("/vehicle/{vin}", response_model=VehicleResponse)
def get_vehicle(vin: str, db: Session = Depends(get_db)):

    vin = vin.upper()
    vehicle = db.query(Vehicle).filter(Vehicle.vin == vin).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


@app.put("/vehicle/{vin}", response_model=VehicleResponse)
def update_vehicle(vin: str, payload: VehicleCreate, db: Session = Depends(get_db)):
    
    """
    Making sure that the VIN in path and body match.
    Replace update of all fields.
    """

    vin = vin.upper()
    if payload.vin != vin:
        raise HTTPException(status_code=422, detail="VIN mismatch between path and body")

    vehicle = db.query(Vehicle).filter(Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    for field, value in payload.dict().items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)
    return vehicle


@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db: Session = Depends(get_db)):
    
    """Deletes a vehicle if it already exists."""

    vin = vin.upper()
    vehicle = db.query(Vehicle).filter(Vehicle.vin == vin).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(vehicle)
    db.commit()
