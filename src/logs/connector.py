from datetime import datetime, date
from sqlalchemy.orm import Session

from src.logs.exceptions import LogNotFoundException
from src.logs.models import DBLog

def get_all_logs(db: Session) -> list[DBLog]:
    logs = db.query(DBLog).all()
    return logs

def create_new_log(db: Session,
                   message: str,
                   timestamp: datetime) -> DBLog:
    log = DBLog(message=message,
                timestamp=timestamp)

    db.add(log)
    db.commit()

    return log

def get_log_by_id(db: Session, log_id: int) -> DBLog:
    log = db.query(DBLog).filter(DBLog.id == log_id).first()

    if log is None:
        raise LogNotFoundException

    return log

def get_log_by_date(db: Session, log_date: date) -> list[DBLog]:
    start_of_day = datetime.combine(log_date, datetime.min.time())
    end_of_day = datetime.combine(log_date, datetime.max.time())

    logs = db.query(DBLog).filter(DBLog.timestamp >= start_of_day, DBLog.timestamp <= end_of_day).all()

    return logs

def delete_all_logs(db: Session):
    db.query(DBLog).delete()
    db.commit()




