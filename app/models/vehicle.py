from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class VehicleBase(BaseModel):
    license_plate: str
    make: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    first_detected_at: datetime
    last_detected_at: datetime
    parking_duration_seconds: Optional[int] = None
    snapshots: Optional[List[str]] = []
    tracking: Optional[Dict] = None
    is_deleted: bool = False

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: Optional[str] = Field(alias="_id") 