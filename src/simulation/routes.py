from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Query, Session
from .packet_simulation import simulate_packets
from src.database.core import get_db
from ..auth.security import get_current_token

router = APIRouter(prefix="/simulate", tags=["simulation"])

@router.get("/{sensor_id}")
async def simulate_for_packets(sensor_id: int,
                               start: str,
                               end: str,
                               db: Session = Depends(get_db),
                               token = Depends(get_current_token)):
    try:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")
        real, simulated = simulate_packets(db, sensor_id, start_date, end_date)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"real": real, "simulated": simulated, "percentage": (real / simulated) * 100}
