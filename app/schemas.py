from pydantic import BaseModel, field_validator, ConfigDict

class VehicleBase(BaseModel):

    """
    Shared fields and validation rules.
    """

    vin: str
    manufacturer_name: str
    description: str | None = None
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str

    @field_validator("vin")
    def normalize_vin(cls, v):

        # Transforms to uppercase in order to stay case-insensitive

        return v.upper()

    @field_validator("horse_power")
    def validate_hp(cls, v):
        if v <= 0:
            raise ValueError("horse_power must be positive")
        return v

    @field_validator("model_year")
    def validate_year(cls, v):

        # Safety range for model years (1886 - 2100, inclusive)

        if not (1886 <= v <= 2100):
            raise ValueError("model_year must be between 1886 and 2100")
        return v

    @field_validator("purchase_price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("purchase_price must be positive")
        return v


class VehicleCreate(VehicleBase):

    """Schema for POST and PUT operations."""

    pass


class VehicleResponse(VehicleBase):

    """ Enables ORM to Pydantic conversion."""

    model_config = ConfigDict(from_attributes=True)
