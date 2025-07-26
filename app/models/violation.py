from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class ViolationBase(BaseModel):
    car_id: str
    parking_space_id: str
    zone_id: str
    type: str
    status: str
    detected_at: datetime
    evidence: List[str] = []
    verification_details: Optional[Dict] = None
    verification_history: Optional[List[Dict]] = None
    enforcement_details: Optional[Dict] = None
    blockchain_record: Optional[Dict] = None
    is_deleted: bool = False

class ViolationCreate(ViolationBase):
    pass

class Violation(ViolationBase):
    id: Optional[str] = Field(alias="_id") 