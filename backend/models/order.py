from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import List, Optional
from .common import PyObjectId
from bson import ObjectId

class OrderStatus(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class OrderItem(BaseModel):
    medicine_id: PyObjectId
    quantity: int = Field(..., gt=0)

class Order(BaseModel):
    pharmacist_id: PyObjectId
    pharmacist_name: str
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    order_date: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})

class OrderInDB(Order):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
