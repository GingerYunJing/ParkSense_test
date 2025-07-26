from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class ZoneBase(BaseModel):
    name: str
    boundaries: Dict
    rules: List[Dict] = []
    is_deleted: bool = False

class ZoneCreate(ZoneBase):
    pass

class Zone(ZoneBase):
    id: Optional[str] = Field(alias="_id")
    created_at: Optional[datetime] = None 