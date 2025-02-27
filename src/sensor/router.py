from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.database.core import get_db
from .connector import get_all_sensors, create_new_sensor, get_sensor_by_code, update_sensor_info, delete_sensor_by_code
from .exceptions import SensorNotFoundException, SensorLocationTakenException, SensorNameTakenException, \
    SensorCodeTakenException
from .schemas import Sensor, SensorCreate, SensorDataOnly, SensorInfoUpdate, SensorInfoOnly
from src.auth.security import get_current_user

api_router = APIRouter(prefix="/sensor", tags=["sensor"])

@api_router.get("/", response_model=list[Sensor])
async def get_sensors_full_info(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_all_sensors(db)

@api_router.post("/", response_model=Sensor)
async def add_sensor(new_sensor: SensorCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        created_sensor = create_new_sensor(db, new_sensor.sensor_code,new_sensor.sensor_name, new_sensor.sensor_location)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    except (SensorLocationTakenException, SensorNameTakenException, SensorCodeTakenException) as e:
        raise HTTPException(409, str(e))

    return created_sensor

@api_router.put("/", response_model=Sensor)
async def update_sensor_info_by_code(new_info: SensorInfoUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        updated_sensor = update_sensor_info(db,new_info.sensor_code,new_info.sensor_name, new_info.sensor_location)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    except (SensorLocationTakenException, SensorNameTakenException) as e:
        raise HTTPException(409, str(e))
    return updated_sensor

@api_router.delete("/{sensor_code}")
async def delete_sensor(sensor_code: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        delete_sensor_by_code(db, sensor_code)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    return {"message": "Sensor deleted successfully!"}

@api_router.get("/{sensor_code}", response_model=Sensor)
async def get_sensor(sensor_code: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        sensor = get_sensor_by_code(db, sensor_code)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    return sensor

@api_router.get("/{sensor_code}/data", response_model=SensorDataOnly)
async def get_sensor_data(sensor_code: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        sensor = get_sensor_by_code(db, sensor_code)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    return sensor

@api_router.get("/{sensor_code}/info", response_model=SensorInfoOnly)
async def get_sensor_info(sensor_code: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        sensor = get_sensor_by_code(db, sensor_code)
    except SensorNotFoundException as e:
        raise HTTPException(404, str(e))
    return sensor
