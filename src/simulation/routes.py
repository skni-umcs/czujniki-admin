from .packet_simulation import simulate_packets, simulate_packets_all
from fastapi import APIRouter, Depends, HTTPException
from .schemas import SimulationResponseSchema, AllSimulationResponseSchema
from ..auth.security import get_current_token
from sqlalchemy.orm import Query, Session
from src.database.core import get_db
from datetime import datetime

router = APIRouter(prefix="/simulate", tags=["simulation"])

@router.get("/all", response_model=AllSimulationResponseSchema)
async def simulate_for_packets(start: str,
                               end: str,
                               db: Session = Depends(get_db),
                               token = Depends(get_current_token)):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")
        results = simulate_packets_all(db, start_date, end_date)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return results

@router.get("/{sensor_id}", response_model=SimulationResponseSchema)
async def simulate_for_packets(sensor_id: int,
                               start: str,
                               end: str,
                               db: Session = Depends(get_db),
                               token = Depends(get_current_token)):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")
        results = simulate_packets(db, sensor_id, start_date, end_date)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return results


