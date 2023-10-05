from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Server(BaseModel):
    server_ip: str = Field(...)
    server_name: str = Field(...)
    num_cpu: int = Field(...)
    total_ram: int = Field(...)
    total_disk: int = Field(...)
    is_active: bool = Field(...)


class ResourceMonitor(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    server_ip: str = Field(...)
    timestamp: str = Field(...)
    cpu: str = Field(...)
    ram: str = Field(...)
    disk: str = Field(...)


class ResourceMonitorCreate(BaseModel):
    server_ip: str = Field(...)
    server_name: str = Field(...)
    num_cpu: int = Field(...)
    total_ram: int = Field(...)
    total_disk: int = Field(...)
    is_active: bool = Field(...)

    id: str = Field(default_factory=ObjectId, alias="_id")
    server_ip: str = Field(...)
    timestamp: str = Field(...)
    cpu: str = Field(...)
    ram: str = Field(...)
    disk: str = Field(...)
