from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional
from .common import PyObjectId
from bson import ObjectId

class Medicine(BaseModel):
    name: str = Field(..., min_length=3)
    manufacturer: str = Field(..., min_length=3)
    stock_quantity: int = Field(..., ge=0) # ge=0 means greater than or equal to 0
    price: float = Field(..., gt=0) # gt=0 means greater than 0
    expiry_date: datetime
    added_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})

class MedicineInDB(Medicine):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

class UpdateMedicine(BaseModel):
    """Model for updating a medicine."""
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    stock_quantity: Optional[int] = None
    price: Optional[float] = None
    expiry_date: Optional[datetime] = None
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})
