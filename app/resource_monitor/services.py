from typing import List, Optional

from bson import ObjectId
from fastapi import status

from app.social.models import AddFollow, UpdateAccountMonitor
from db.init_db import get_collection_client
import pymongo
from datetime import datetime, timedelta

servers_client = get_collection_client("servers")
resource_monitors_client = get_collection_client("resource_monitors")


async def insert_resource_monitors(server, resource_monitor):
    server_query = {"server_ip": server["server_ip"]}
    server_rp = await servers_client.find_one(server_query)
    if server_rp == None:
        await servers_client.insert_one(server)
    await resource_monitors_client.insert_one(resource_monitor)


async def get_average_monitor():
    try:
        all_servers = servers_client.find({})

        total_num_cpu = 0
        total_ram = 0
        total_disk = 0
        total_used_cpu = 0
        total_used_ram = 0
        total_used_disk = 0
        total_count = 0

        one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async for server in all_servers:
            last_resource_monitor = None
            total_count += 1
            total_num_cpu += server["num_cpu"]
            total_ram += server["total_ram"]
            total_disk += server["total_disk"]
            query = {
                "timestamp": {"$gte": one_hour_ago, "$lte": current_time},
                "server_ip": server["server_ip"],
            }
            sort = [("timestamp", -1)]

            last_resource_monitor = await resource_monitors_client.find_one(
                filter=query, sort=sort
            )
            if last_resource_monitor != None:
                total_used_cpu += float(last_resource_monitor["cpu"])
                total_used_ram += float(last_resource_monitor["ram"])
                total_used_disk += float(last_resource_monitor["disk"])

        cpu_percent = total_used_cpu / total_count
        ram_percent = (total_used_ram / total_ram) * 100
        disk_percent = (total_used_disk / total_disk) * 100
        print(cpu_percent)
        print(ram_percent)
        print(disk_percent)
        data = {
            "cpu_percent": cpu_percent,
            "ram_percent": ram_percent,
            "disk_percent": disk_percent,
        }
        return data
    except Exception:
        data = {
            "cpu_percent": cpu_percent,
            "ram_percent": ram_percent,
            "disk_percent": disk_percent,
        }


async def get_server_details():
    try:
        all_servers = servers_client.find({})
        total_count = 0
        one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        server_details = []

        async for server in all_servers:
            last_resource_monitor = None
            is_active = False
            cpu_percent = 0
            disk_percent = 0
            ram_percent = 0
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            total_count += 1

            query = {
                "timestamp": {"$gte": one_hour_ago, "$lte": current_time},
                "server_ip": server["server_ip"],
            }
            sort = [("timestamp", -1)]
            last_resource_monitor = await resource_monitors_client.find_one(
                filter=query,
                sort=sort,
            )
            if last_resource_monitor != None:
                is_active = True
                cpu_percent = last_resource_monitor["cpu"]
                disk_percent = (
                    float(last_resource_monitor["disk"])
                    / float(server["total_disk"])
                    * 100
                )
                ram_percent = (
                    float(last_resource_monitor["ram"])
                    / float(server["total_ram"])
                    * 100
                )
                timestamp = last_resource_monitor["timestamp"]
            server_detail = {
                "server_ip": server["server_ip"],
                "server_name": server["server_name"],
                "cpu_percent": cpu_percent,
                "ram_percent": ram_percent,
                "disk_percent": disk_percent,
                "is_active": is_active,
                "timestamp": timestamp,
            }
            server_details.append(server_detail)
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "count": total_count,
            "server_details": server_details,
        }
        return data

    except:
        raise
