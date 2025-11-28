from datetime import datetime
from .manager import service_manager, sensor_manager
from ..sensor.connector import get_all_sensors, get_sensor_by_id
from ..database.core import get_db_session
import json

from ..sensor_data.connector import get_graph


def sensors_as_dict():
    with get_db_session() as db:

        sensors = get_all_sensors(db)

        active = len([sensor for sensor in sensors if sensor.sensor_status == 1])
        inactive = len(sensors) - active

        sensors_dict = {"timestamp": str(datetime.now()), "total": len(sensors), "sensors" :[], "online": active, "offline": inactive}

        for sensor in sensors:
            sensors_dict["sensors"].append({
                "sensor_id": sensor.sensor_id,
                "status": "online" if sensor.sensor_status == 1 else "offline",
                "last_seen": str(datetime.fromtimestamp(sensor.last_message_timestamp)) if sensor.last_message_timestamp else None,
                "sensor_type": sensor.last_message_type,
                "seconds_ago": int(datetime.now().timestamp() - sensor.last_message_timestamp) if sensor.last_message_timestamp else None
            })

    return sensors_dict

def network_graph(sensor_id:int):
    with get_db_session() as db:
        sensor = get_sensor_by_id(db, sensor_id)
        graph = get_graph(db, sensor.last_sensor_data_id)
    return graph

async def push_sensor_update():
    data = sensors_as_dict()
    json_data = json.dumps(data)
    await sensor_manager.broadcast(json_data)

async def push_service_update(sensor_id: int):
    graph = network_graph(sensor_id)
    json_data = json.dumps(graph)
    await service_manager.broadcast(json_data)

