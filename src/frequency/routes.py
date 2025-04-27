from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.core import get_db
from .connector import get_current_frequency_period_by_sensor_id
from ..frequency.connector import get_frequency_periods_all, \
    get_frequency_periods_by_sensor_id, get_current_frequencies

router = APIRouter(prefix="/frequency", tags=["frequency"])

@router.get("/")
async def get_all_frequency_periods(db: Session = Depends(get_db)):
    try:
        frequencies = get_frequency_periods_all(db)
    except Exception as e:
        raise HTTPException(404, str(e))
    return frequencies

@router.get("/currents")
async def get_all_current_frequency_periods(db: Session = Depends(get_db)):
    try:
        frequencies = get_current_frequencies(db)
    except Exception as e:
        raise HTTPException(404, str(e))
    return frequencies

@router.get("/{sensor_id}")
async def get_all_frequency_periods_for_sensor(sensor_id: int, db: Session = Depends(get_db)):
    try:
        frequencies = get_frequency_periods_by_sensor_id(db,sensor_id)
    except Exception as e:
        raise HTTPException(404, str(e))
    return frequencies

@router.get("/{sensor_id}/current")
async def get_current_frequency_period_for_sensor(sensor_id: int, db: Session = Depends(get_db)):
    try:
        frequency = get_current_frequency_period_by_sensor_id(db, sensor_id)
    except Exception as e:
        raise HTTPException(404, str(e))
    return frequency

