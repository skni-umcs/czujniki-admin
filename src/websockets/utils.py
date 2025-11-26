from datetime import datetime
from .manager import manager
from ..sensor.connector import get_all_sensors
from ..database.core import get_db_session
import json

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

async def push_update():
    data = sensors_as_dict()
    json_data = json.dumps(data)
    await manager.broadcast(json_data)