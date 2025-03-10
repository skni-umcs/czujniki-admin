from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.mqtt_handler import publish_message
from config import Settings
from src.database.core import get_db
from .connector import get_all_sensors, create_new_sensor, get_sensor_by_code, update_sensor_info, delete_sensor_by_code
from .exceptions import SensorNotFoundException, SensorLocationTakenException, SensorNameTakenException, \
    SensorIdTakenException, SensorFrequencyNotWithinLimit
from .schemas import Sensor, SensorCreate, SensorDataOnly, SensorInfoUpdate, SensorInfoOnly, SensorFrequencyOnly
from src.auth.security import get_current_user
from ..logs.logger import Logger
from ..user.models import DBUser

api_router = APIRouter(prefix="/sensor", tags=["sensor"])
settings = Settings()

@api_router.get("/", response_model=list[Sensor])
async def get_sensors_full_info(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_all_sensors(db)

@api_router.post("/", response_model=Sensor)
async def add_sensor(new_sensor: SensorCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    try:
        created_sensor = create_new_sensor(db, new_sensor.sensor_id,new_sensor.sensor_name, new_sensor.sensor_location, new_sensor.sensor_frequency)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    except (SensorLocationTakenException, SensorNameTakenException, SensorIdTakenException) as e:
        raise HTTPException(409, str(e))
    except SensorFrequencyNotWithinLimit as e:
        raise HTTPException(400, str(e))
    Logger.write(f"New sensor added: {created_sensor.sensor_id} by {current_user.login}")
    return created_sensor

@api_router.put("/", response_model=Sensor)
async def update_sensor_info_by_code(new_info: SensorInfoUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        updated_sensor = update_sensor_info(db,new_info.sensor_id,new_info.sensor_name, new_info.sensor_location, new_info.sensor_frequency)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    except (SensorLocationTakenException, SensorNameTakenException) as e:
        raise HTTPException(409, str(e))
    except SensorFrequencyNotWithinLimit as e:
        raise HTTPException(400, str(e))

    if new_info.sensor_frequency:
        message_dict = {'sensor_id': new_info.sensor_id, 'sensor_frequency': new_info.sensor_frequency}
        publish_message(message_dict)

    return updated_sensor


@api_router.get("/frequencies", response_model=list[SensorFrequencyOnly])
async def get_sensors_frequnecies(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    sensors = get_all_sensors(db)
    return sensors

@api_router.delete("/{sensor_id}")
async def delete_sensor(sensor_id: str, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    try:
        delete_sensor_by_code(db, sensor_id)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    Logger.write(f"Sensor deleted: {sensor_id} by {current_user.login}")
    return {"message": "Sensor deleted successfully!"}

@api_router.get("/{sensor_id}", response_model=Sensor)
async def get_sensor(sensor_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    return sensor



@api_router.get("/{sensor_id}/data", response_model=SensorDataOnly)
async def get_sensor_data(sensor_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    return sensor

@api_router.get("/{sensor_id}/info", response_model=SensorInfoOnly)
async def get_sensor_info(sensor_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        sensor = get_sensor_by_code(db, sensor_id)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    return sensor



