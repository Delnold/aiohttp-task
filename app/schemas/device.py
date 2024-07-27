from pydantic import BaseModel, Field
from typing import Optional


class DeviceCreate(BaseModel):
    name: str
    type: str
    login: str
    password: str
    location_id: Optional[str] = None

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
    location_id: Optional[str] = None
