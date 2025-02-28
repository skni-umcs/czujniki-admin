from datetime import date
from http.client import HTTPException
from fastapi import Depends, APIRouter, Query
from .connector import get_all_logs, get_log_by_date, delete_all_logs
from .schemas import LogDate, Log
from ..database.core import get_db
from ..auth.security import get_current_user

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/", response_model=list[Log])
async def get_logs(db = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        logs = get_all_logs(db)
    except Exception as e:
        raise HTTPException(500, str(e))
    return logs

@router.get("/day", response_model=list[Log])
async def get_logs_by_day(log_date: date = Query(..., description="Date in YYYY-MM-DD format to filter logs"), db = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        logs = get_log_by_date(db, log_date)
    except Exception as e:
        raise HTTPException(500, str(e))
    return logs

@router.delete("/")
async def delete_logs(db = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        delete_all_logs(db)
    except Exception as e:
        raise HTTPException(500, str(e))
    return {"message": "Logs deleted successfully!"}
