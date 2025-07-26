from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.vehicle import Vehicle, VehicleCreate
from app.db import get_database
from typing import List, Optional
from app.auth import get_current_user, get_current_admin_user

router = APIRouter()

@router.post("/vehicles", response_model=Vehicle, dependencies=[Depends(get_current_user)])
async def create_vehicle(vehicle: VehicleCreate):
    db = get_database()
    vehicle_dict = vehicle.dict()
    result = await db["vehicles"].insert_one(vehicle_dict)
    vehicle_dict["_id"] = str(result.inserted_id)
    return Vehicle(**vehicle_dict)

@router.post("/vehicles/bulk", response_model=List[Vehicle], dependencies=[Depends(get_current_admin_user)])
async def create_vehicles_bulk(vehicles: List[VehicleCreate]):
    db = get_database()
    vehicle_dicts = [v.dict() for v in vehicles]
    result = await db["vehicles"].insert_many(vehicle_dicts)
    inserted = []
    for _id, v in zip(result.inserted_ids, vehicle_dicts):
        v["_id"] = str(_id)
        inserted.append(Vehicle(**v))
    return inserted

@router.get("/vehicles", dependencies=[Depends(get_current_user)])
async def list_vehicles(
    license_plate: Optional[str] = None,
    make: Optional[str] = None,
    model: Optional[str] = None,
    color: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "first_detected_at",
    order: int = -1
):
    db = get_database()
    query = {"is_deleted": False}
    if license_plate:
        query["license_plate"] = license_plate
    if make:
        query["make"] = make
    if model:
        query["model"] = model
    if color:
        query["color"] = color
    total = await db["vehicles"].count_documents(query)
    vehicles = []
    cursor = db["vehicles"].find(query).sort(sort_by, order).skip(skip).limit(limit)
    async for v in cursor:
        v["_id"] = str(v["_id"])
        vehicles.append(Vehicle(**v))
    return {"items": vehicles, "total": total}

@router.get("/vehicles/{vehicle_id}", response_model=Vehicle, dependencies=[Depends(get_current_user)])
async def get_vehicle(vehicle_id: str):
    db = get_database()
    v = await db["vehicles"].find_one({"_id": vehicle_id, "is_deleted": False})
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    v["_id"] = str(v["_id"])
    return Vehicle(**v)

@router.put("/vehicles/{vehicle_id}", response_model=Vehicle, dependencies=[Depends(get_current_user)])
async def update_vehicle(vehicle_id: str, vehicle: VehicleCreate):
    db = get_database()
    update_data = vehicle.dict()
    if "is_deleted" in update_data:
        del update_data["is_deleted"]
    result = await db["vehicles"].update_one({"_id": vehicle_id, "is_deleted": False}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    v = await db["vehicles"].find_one({"_id": vehicle_id})
    v["_id"] = str(v["_id"])
    return Vehicle(**v)

@router.delete("/vehicles/{vehicle_id}", dependencies=[Depends(get_current_admin_user)])
async def delete_vehicle(vehicle_id: str):
    db = get_database()
    result = await db["vehicles"].update_one({"_id": vehicle_id, "is_deleted": False}, {"$set": {"is_deleted": True}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"detail": "Vehicle soft deleted"} 