from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    ADMIN = "Admin"
    SUPPLIER = "Supplier"
    PHARMACIST = "Pharmacist"

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserInDB(User):
    id: str # This will be the MongoDB `_id`
