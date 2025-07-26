from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ParkingSpaceBase(BaseModel):
    zone_id: str
    type: str
    status: str
    occupied_by_car_id: Optional[str] = None
    occupied_since: Optional[datetime] = None
    current_parking_duration_seconds: Optional[int] = None
    associated_violation_ids: Optional[List[str]] = []
    is_deleted: bool = False

class ParkingSpaceCreate(ParkingSpaceBase):
    pass

class ParkingSpace(ParkingSpaceBase):
    id: Optional[str] = Field(alias="_id") 