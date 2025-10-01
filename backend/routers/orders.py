from fastapi import APIRouter, Depends, HTTPException, status, Body
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClientSession
from typing import List
from datetime import datetime

from database import db
from models.order import Order, OrderInDB, OrderItem, OrderStatus
from models.common import PyObjectId

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

# Dependency to get the database instance
def get_database() -> AsyncIOMotorDatabase:
    return db.db

@router.post("/", response_model=OrderInDB, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: Order = Body(...),
    database: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a new order.
    This transactionally checks for stock and decrements it before creating the order.
    """
    async with await db.client.start_session() as session:
        async with session.in_transaction():
            for item in order_data.items:
                medicine = await database.medicines.find_one(
                    {"_id": item.medicine_id},
                    session=session
                )
                if not medicine:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Medicine with id {item.medicine_id} not found."
                    )
                if medicine['stock_quantity'] < item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Not enough stock for {medicine['name']}. Available: {medicine['stock_quantity']}, Requested: {item.quantity}"
                    )

                # Decrement stock
                await database.medicines.update_one(
                    {"_id": item.medicine_id},
                    {"$inc": {"stock_quantity": -item.quantity}},
                    session=session
                )

            # All stock checks and decrements passed, now create the order
            new_order = await database.orders.insert_one(
                order_data.model_dump(by_alias=False),
                session=session
            )
            created_order = await database.orders.find_one(
                {"_id": new_order.inserted_id},
                session=session
            )
            return created_order

@router.get("/", response_model=List[OrderInDB])
async def list_orders(database: AsyncIOMotorDatabase = Depends(get_database)):
    """List all orders."""
    orders = await database.orders.find().to_list(1000)
    return orders

@router.get("/{id}", response_model=OrderInDB)
async def get_order(id: PyObjectId, database: AsyncIOMotorDatabase = Depends(get_database)):
    """Get a single order by its ID."""
    order = await database.orders.find_one({"_id": id})
    if order:
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")

@router.patch("/{id}/status", response_model=OrderInDB)
async def update_order_status(
    id: PyObjectId,
    status_update: OrderStatus = Body(..., embed=True),
    database: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update an order's status (e.g., from 'Pending' to 'Shipped')."""
    from pymongo import ReturnDocument

    updated_order = await database.orders.find_one_and_update(
        {"_id": id},
        {"$set": {"status": status_update, "last_updated": datetime.utcnow()}},
        return_document=ReturnDocument.AFTER
    )

    if updated_order:
        return updated_order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")