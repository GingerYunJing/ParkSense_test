from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.zone import Zone, ZoneCreate
from app.db import get_database
from datetime import datetime
from typing import List, Optional
from app.auth import get_current_user, get_current_admin_user

router = APIRouter()

@router.post("/zones", response_model=Zone, dependencies=[Depends(get_current_user)])
async def create_zone(zone: ZoneCreate):
    db = get_database()
    zone_dict = zone.dict()
    zone_dict["created_at"] = datetime.utcnow()
    result = await db["zones"].insert_one(zone_dict)
    zone_dict["_id"] = str(result.inserted_id)
    return Zone(**zone_dict)

@router.post("/zones/bulk", response_model=List[Zone], dependencies=[Depends(get_current_admin_user)])
async def create_zones_bulk(zones: List[ZoneCreate]):
    db = get_database()
    zone_dicts = [z.dict() for z in zones]
    for z in zone_dicts:
        z["created_at"] = datetime.utcnow()
    result = await db["zones"].insert_many(zone_dicts)
    inserted = []
    for _id, z in zip(result.inserted_ids, zone_dicts):
        z["_id"] = str(_id)
        inserted.append(Zone(**z))
    return inserted

@router.get("/zones", dependencies=[Depends(get_current_user)])
async def list_zones(
    name: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "created_at",
    order: int = -1
):
    db = get_database()
    query = {"is_deleted": False}
    if name:
        query["name"] = name
    total = await db["zones"].count_documents(query)
    zones = []
    cursor = db["zones"].find(query).sort(sort_by, order).skip(skip).limit(limit)
    async for z in cursor:
        z["_id"] = str(z["_id"])
        zones.append(Zone(**z))
    return {"items": zones, "total": total}

@router.get("/zones/{zone_id}", response_model=Zone, dependencies=[Depends(get_current_user)])
async def get_zone(zone_id: str):
    db = get_database()
    z = await db["zones"].find_one({"_id": zone_id, "is_deleted": False})
    if not z:
        raise HTTPException(status_code=404, detail="Zone not found")
    z["_id"] = str(z["_id"])
    return Zone(**z)

@router.put("/zones/{zone_id}", response_model=Zone, dependencies=[Depends(get_current_user)])
async def update_zone(zone_id: str, zone: ZoneCreate):
    db = get_database()
    update_data = zone.dict()
    if "is_deleted" in update_data:
        del update_data["is_deleted"]
    result = await db["zones"].update_one({"_id": zone_id, "is_deleted": False}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Zone not found")
    z = await db["zones"].find_one({"_id": zone_id})
    z["_id"] = str(z["_id"])
    return Zone(**z)

@router.delete("/zones/{zone_id}", dependencies=[Depends(get_current_admin_user)])
async def delete_zone(zone_id: str):
    db = get_database()
    result = await db["zones"].update_one(
        {"_id": zone_id, "is_deleted": False}, {"$set": {"is_deleted": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Zone not found")
    return {"detail": "Zone soft deleted"} 