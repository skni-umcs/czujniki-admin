from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from config import Settings
from src.database.core import get_db
from .connector import get_all_sensors, get_sensor_by_id, calculate_climate_delays
from .exceptions import SensorNotFoundException
from .schemas import Sensor, SensorDelay
from ..auth.security import get_current_token

api_router = APIRouter(prefix="/sensor", tags=["sensor"])
settings = Settings()

@api_router.get("/", response_model=list[Sensor])
async def get_sensors_full_info(db: Session = Depends(get_db), token = Depends(get_current_token)):
    return get_all_sensors(db)

@api_router.get("/delays", response_model=list[SensorDelay])
async def get_sensors_delays(db: Session = Depends(get_db), token = Depends(get_current_token)):
    result = calculate_climate_delays(db)
    return result

@api_router.get("/{sensor_id}", response_model=Sensor)
async def get_sensor(sensor_id: int, db: Session = Depends(get_db), token = Depends(get_current_token)):
    try:
        sensor = get_sensor_by_id(db, sensor_id)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    return sensor



