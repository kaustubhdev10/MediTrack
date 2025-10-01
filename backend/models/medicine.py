from pydantic import BaseModel, Field
from datetime import date, datetime

class Medicine(BaseModel):
    name: str = Field(..., min_length=3)
    manufacturer: str = Field(..., min_length=3)
    stock_quantity: int = Field(..., ge=0) # ge=0 means greater than or equal to 0
    price: float = Field(..., gt=0) # gt=0 means greater than 0
    expiry_date: date
    added_at: datetime = Field(default_factory=datetime.utcnow)

class MedicineInDB(Medicine):
    id: str # This will be the MongoDB `_id`
