from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List

class OrderStatus(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class OrderItem(BaseModel):
    medicine_id: str
    quantity: int = Field(..., gt=0)

class Order(BaseModel):
    pharmacist_id: str
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    order_date: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
