from fastapi import APIRouter, Depends, HTTPException, status, Body
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from bson import ObjectId
from pymongo import ReturnDocument

from database import db
from models.medicine import Medicine, MedicineInDB, UpdateMedicine
from models.common import PyObjectId

router = APIRouter(
    prefix="/medicines",
    tags=["Medicines"],
)

# Dependency to get the database instance
def get_database() -> AsyncIOMotorDatabase:
    return db.db

@router.post("/", response_model=MedicineInDB, status_code=status.HTTP_201_CREATED)
async def create_medicine(
    medicine: Medicine = Body(...),
    database: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new medicine in the inventory."""
    new_medicine = await database.medicines.insert_one(medicine.model_dump(by_alias=False))
    created_medicine = await database.medicines.find_one({"_id": new_medicine.inserted_id})
    return created_medicine

@router.get("/", response_model=List[MedicineInDB])
async def list_medicines(database: AsyncIOMotorDatabase = Depends(get_database)):
    """List all medicines in the inventory."""
    medicines = await database.medicines.find().to_list(1000)
    return medicines

@router.get("/{id}", response_model=MedicineInDB)
async def get_medicine(id: PyObjectId, database: AsyncIOMotorDatabase = Depends(get_database)):
    """Get a single medicine by its ID."""
    medicine = await database.medicines.find_one({"_id": id})
    if medicine:
        return medicine
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with id {id} not found")

@router.put("/{id}", response_model=MedicineInDB)
async def update_medicine(
    id: PyObjectId,
    medicine_update: UpdateMedicine = Body(...),
    database: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a medicine's details."""
    update_data = medicine_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided")

    updated_medicine = await database.medicines.find_one_and_update(
        {"_id": id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )

    if updated_medicine:
        return updated_medicine
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with id {id} not found")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicine(id: PyObjectId, database: AsyncIOMotorDatabase = Depends(get_database)):
    """Delete a medicine from the inventory."""
    delete_result = await database.medicines.delete_one({"_id": id})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with id {id} not found")

    return