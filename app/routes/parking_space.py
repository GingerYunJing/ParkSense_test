from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.parking_space import ParkingSpace, ParkingSpaceCreate
from app.db import get_database
from typing import List, Optional
from app.auth import get_current_user, get_current_admin_user

router = APIRouter()

@router.post("/parking-spaces", response_model=ParkingSpace, dependencies=[Depends(get_current_user)])
async def create_parking_space(space: ParkingSpaceCreate):
    db = get_database()
    space_dict = space.dict()
    result = await db["parking_spaces"].insert_one(space_dict)
    space_dict["_id"] = str(result.inserted_id)
    return ParkingSpace(**space_dict)

@router.post("/parking-spaces/bulk", response_model=List[ParkingSpace], dependencies=[Depends(get_current_admin_user)])
async def create_parking_spaces_bulk(spaces: List[ParkingSpaceCreate]):
    db = get_database()
    space_dicts = [s.dict() for s in spaces]
    result = await db["parking_spaces"].insert_many(space_dicts)
    inserted = []
    for _id, s in zip(result.inserted_ids, space_dicts):
        s["_id"] = str(_id)
        inserted.append(ParkingSpace(**s))
    return inserted

@router.get("/parking-spaces", dependencies=[Depends(get_current_user)])
async def list_parking_spaces(
    zone_id: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "zone_id",
    order: int = -1
):
    db = get_database()
    query = {"is_deleted": False}
    if zone_id:
        query["zone_id"] = zone_id
    if type:
        query["type"] = type
    if status:
        query["status"] = status
    total = await db["parking_spaces"].count_documents(query)
    spaces = []
    cursor = db["parking_spaces"].find(query).sort(sort_by, order).skip(skip).limit(limit)
    async for s in cursor:
        s["_id"] = str(s["_id"])
        spaces.append(ParkingSpace(**s))
    return {"items": spaces, "total": total}

@router.get("/parking-spaces/{space_id}", response_model=ParkingSpace, dependencies=[Depends(get_current_user)])
async def get_parking_space(space_id: str):
    db = get_database()
    s = await db["parking_spaces"].find_one({"_id": space_id, "is_deleted": False})
    if not s:
        raise HTTPException(status_code=404, detail="Parking space not found")
    s["_id"] = str(s["_id"])
    return ParkingSpace(**s)

@router.put("/parking-spaces/{space_id}", response_model=ParkingSpace, dependencies=[Depends(get_current_user)])
async def update_parking_space(space_id: str, space: ParkingSpaceCreate):
    db = get_database()
    update_data = space.dict()
    if "is_deleted" in update_data:
        del update_data["is_deleted"]
    result = await db["parking_spaces"].update_one({"_id": space_id, "is_deleted": False}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Parking space not found")
    s = await db["parking_spaces"].find_one({"_id": space_id})
    s["_id"] = str(s["_id"])
    return ParkingSpace(**s)

@router.delete("/parking-spaces/{space_id}", dependencies=[Depends(get_current_admin_user)])
async def delete_parking_space(space_id: str):
    db = get_database()
    result = await db["parking_spaces"].update_one({"_id": space_id, "is_deleted": False}, {"$set": {"is_deleted": True}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Parking space not found")
    return {"detail": "Parking space soft deleted"} 