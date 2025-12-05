from sqlalchemy import Column, String, Integer, Float
from app.database import Base

class Vehicle(Base):

    """
    ORM models are mapped to the vehicles table,
    VIN is stored in its uppercase format and used as the primary key
    """
    
    __tablename__ = "vehicles"

    vin = Column(String, primary_key=True, index=True)
    manufacturer_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    horse_power = Column(Integer, nullable=False)
    model_name = Column(String, nullable=False)
    model_year = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    fuel_type = Column(String, nullable=False)
