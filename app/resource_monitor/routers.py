from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Path, status
from fastapi.responses import JSONResponse

from app.resource_monitor.models import Server, ResourceMonitor, ResourceMonitorCreate

from app.resource_monitor.services import (
    insert_resource_monitors,
    get_a_server as get_server,
    get_average_monitor as get_avg_monitor_service,
)
from app.resource_monitor import services

router = APIRouter()


@router.post("/schedule-update")
async def create_insert_resource_monitor(body: ResourceMonitorCreate):
    print(type(body))
    # resource_create_dict = body.dict()
    server_ip = body.server_ip  # resource_create_dict["server_ip"]
    print(server_ip)
    server_name = body.server_name
    num_cpu = body.num_cpu
    total_ram = body.total_ram
    total_disk = body.total_disk
    is_active = body.is_active
    # # id = resource_create_dict["id"]
    timestamp = body.timestamp
    cpu = body.cpu
    ram = body.ram
    disk = body.disk

    server = Server(
        server_ip=server_ip,
        server_name=server_name,
        num_cpu=num_cpu,
        total_ram=total_ram,
        total_disk=total_disk,
        is_active=is_active,
    )
    resource_monitor = ResourceMonitor(
        id=id, server_ip=server_ip, timestamp=timestamp, cpu=cpu, ram=ram, disk=disk
    )
    await insert_resource_monitors(server.dict(), resource_monitor.dict())
    return {"message": "update successfully!"}


@router.get("/get-server")
async def get_a_server():
    server = await get_server()
    return server


@router.get("/get-average-monitor")
async def get_average_monitor():
    data = await get_avg_monitor_service()
    return data


@router.get("/get-server-details")
async def get_server_details():
    data = await services.get_server_details()
    return data
