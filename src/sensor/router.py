from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.dependecies import get_db
from .connector import get_all_sensors, create_new_sensor, update_sensor_by_index, get_sensor_by_code, unwrap_rssi
from .schemas import Sensor, SensorCreate, SensorUpdate, RSSIData, Sensor
from src.auth.security import get_current_user

api_router = APIRouter(prefix="/sensor", tags=["sensor"])

# TODO: Add authentication to the endpoints
@api_router.get("/", response_model=list[Sensor])
async def get_sensors(db: Session = Depends(get_db),):
    return get_all_sensors(db)


@api_router.post("/", response_model=Sensor)
async def add_sensor(new_sensor: SensorCreate, db: Session = Depends(get_db), ):
    try:
        created_sensor = create_new_sensor(db, new_sensor)

    except Exception as e:
        raise HTTPException(404, str(e))

    return created_sensor


@api_router.post("/receive_rssi")
async def receive_rssi(rssi_data: RSSIData, db: Session = Depends(get_db), ):
    try:
        unwrap_rssi(db, rssi_data.sensor_code, rssi_data.rssi, rssi_data.timestamp)
    except Exception as e:
        raise HTTPException(404, str(e))

    return {"message": "RSSI data received"}


@api_router.get("/{sensor_code}", response_model=Sensor)
async def get_sensor(sensor_code: str, db: Session = Depends(get_db), ):
    try:
        sensor = get_sensor_by_code(db, sensor_code)
    except Exception as e:
        raise HTTPException(404, str(e))

    return sensor

@api_router.put("/{sensor_code}", response_model=Sensor)
async def update_sensor(sensor_code: str, updated_sensor: SensorUpdate, db: Session = Depends(get_db),
                        ):
    try:
        sensor_after_update = update_sensor_by_index(db, sensor_code, updated_sensor)
    except Exception as e:
        raise HTTPException(404, str(e))

    return sensor_after_update
