from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional
from .common import PyObjectId
from bson import ObjectId

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
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})

class UserInDB(User):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

class UserCreate(BaseModel):
    """Model for creating a user, received from the API."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole

class UserPublic(BaseModel):
    """Model for user data that is safe to be returned to clients."""
    id: PyObjectId = Field(alias="_id")
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})

class Token(BaseModel):
    access_token: str
    token_type: str
