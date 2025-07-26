from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.violation import Violation, ViolationCreate
from app.db import get_database
from typing import List, Optional
from app.auth import get_current_user, get_current_admin_user

router = APIRouter()

@router.post("/violations", response_model=Violation, dependencies=[Depends(get_current_user)])
async def create_violation(violation: ViolationCreate):
    db = get_database()
    violation_dict = violation.dict()
    result = await db["violations"].insert_one(violation_dict)
    violation_dict["_id"] = str(result.inserted_id)
    return Violation(**violation_dict)

@router.post("/violations/bulk", response_model=List[Violation], dependencies=[Depends(get_current_admin_user)])
async def create_violations_bulk(violations: List[ViolationCreate]):
    db = get_database()
    violation_dicts = [v.dict() for v in violations]
    result = await db["violations"].insert_many(violation_dicts)
    inserted = []
    for _id, v in zip(result.inserted_ids, violation_dicts):
        v["_id"] = str(_id)
        inserted.append(Violation(**v))
    return inserted

@router.get("/violations", dependencies=[Depends(get_current_user)])
async def list_violations(
    car_id: Optional[str] = None,
    parking_space_id: Optional[str] = None,
    zone_id: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "detected_at",
    order: int = -1
):
    db = get_database()
    query = {"is_deleted": False}
    if car_id:
        query["car_id"] = car_id
    if parking_space_id:
        query["parking_space_id"] = parking_space_id
    if zone_id:
        query["zone_id"] = zone_id
    if type:
        query["type"] = type
    if status:
        query["status"] = status
    total = await db["violations"].count_documents(query)
    violations = []
    cursor = db["violations"].find(query).sort(sort_by, order).skip(skip).limit(limit)
    async for v in cursor:
        v["_id"] = str(v["_id"])
        violations.append(Violation(**v))
    return {"items": violations, "total": total}

@router.get("/violations/{violation_id}", response_model=Violation, dependencies=[Depends(get_current_user)])
async def get_violation(violation_id: str):
    db = get_database()
    v = await db["violations"].find_one({"_id": violation_id, "is_deleted": False})
    if not v:
        raise HTTPException(status_code=404, detail="Violation not found")
    v["_id"] = str(v["_id"])
    return Violation(**v)

@router.put("/violations/{violation_id}", response_model=Violation, dependencies=[Depends(get_current_user)])
async def update_violation(violation_id: str, violation: ViolationCreate):
    db = get_database()
    update_data = violation.dict()
    if "is_deleted" in update_data:
        del update_data["is_deleted"]
    result = await db["violations"].update_one({"_id": violation_id, "is_deleted": False}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Violation not found")
    v = await db["violations"].find_one({"_id": violation_id})
    v["_id"] = str(v["_id"])
    return Violation(**v)

@router.delete("/violations/{violation_id}", dependencies=[Depends(get_current_admin_user)])
async def delete_violation(violation_id: str):
    db = get_database()
    result = await db["violations"].update_one({"_id": violation_id, "is_deleted": False}, {"$set": {"is_deleted": True}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Violation not found")
    return {"detail": "Violation soft deleted"} 