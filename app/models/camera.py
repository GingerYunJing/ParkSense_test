from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class CameraBase(BaseModel):
    zone_id: str
    name: str
    configuration: Optional[Dict] = None
    health: Optional[Dict] = None
    status: str = "offline"
    is_deleted: bool = False

class CameraCreate(CameraBase):
    pass

class Camera(CameraBase):
    id: Optional[str] = Field(alias="_id")
    created_at: Optional[datetime] = None 