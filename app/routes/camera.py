from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.camera import Camera, CameraCreate
from app.db import get_database
from datetime import datetime
from typing import List, Optional
from app.auth import get_current_user, get_current_admin_user

router = APIRouter()

@router.post("/cameras", response_model=Camera, dependencies=[Depends(get_current_user)])
async def create_camera(camera: CameraCreate):
    db = get_database()
    camera_dict = camera.dict()
    camera_dict["created_at"] = datetime.utcnow()
    result = await db["cameras"].insert_one(camera_dict)
    camera_dict["_id"] = str(result.inserted_id)
    return Camera(**camera_dict)

@router.post("/cameras/bulk", response_model=List[Camera], dependencies=[Depends(get_current_admin_user)])
async def create_cameras_bulk(cameras: List[CameraCreate]):
    db = get_database()
    camera_dicts = [c.dict() for c in cameras]
    for c in camera_dicts:
        c["created_at"] = datetime.utcnow()
    result = await db["cameras"].insert_many(camera_dicts)
    inserted = []
    for _id, c in zip(result.inserted_ids, camera_dicts):
        c["_id"] = str(_id)
        inserted.append(Camera(**c))
    return inserted

@router.get("/cameras", dependencies=[Depends(get_current_user)])
async def list_cameras(
    zone_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "created_at",
    order: int = -1
):
    db = get_database()
    query = {"is_deleted": False}
    if zone_id:
        query["zone_id"] = zone_id
    total = await db["cameras"].count_documents(query)
    cameras = []
    cursor = db["cameras"].find(query).sort(sort_by, order).skip(skip).limit(limit)
    async for c in cursor:
        c["_id"] = str(c["_id"])
        cameras.append(Camera(**c))
    return {"items": cameras, "total": total}

@router.get("/cameras/{camera_id}", response_model=Camera, dependencies=[Depends(get_current_user)])
async def get_camera(camera_id: str):
    db = get_database()
    cam = await db["cameras"].find_one({"_id": camera_id, "is_deleted": False})
    if not cam:
        raise HTTPException(status_code=404, detail="Camera not found")
    cam["_id"] = str(cam["_id"])
    return Camera(**cam)

@router.put("/cameras/{camera_id}", response_model=Camera, dependencies=[Depends(get_current_user)])
async def update_camera(camera_id: str, camera: CameraCreate):
    db = get_database()
    update_data = camera.dict()
    if "is_deleted" in update_data:
        del update_data["is_deleted"]
    result = await db["cameras"].update_one({"_id": camera_id, "is_deleted": False}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Camera not found")
    cam = await db["cameras"].find_one({"_id": camera_id})
    cam["_id"] = str(cam["_id"])
    return Camera(**cam)

@router.delete("/cameras/{camera_id}", dependencies=[Depends(get_current_admin_user)])
async def delete_camera(camera_id: str):
    db = get_database()
    result = await db["cameras"].update_one({"_id": camera_id, "is_deleted": False}, {"$set": {"is_deleted": True}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Camera not found")
    return {"detail": "Camera soft deleted"} 