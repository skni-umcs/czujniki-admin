from datetime import datetime

from .models import DBModule
from sqlalchemy.orm import Session
from .schemas import ModuleCreate, ModuleUpdate


def get_all_modules(db: Session) -> list[DBModule]:
    modules = db.query(DBModule).all()
    return modules


def create_new_module(db: Session, module_to_add: ModuleCreate) -> DBModule:

    code_err = db.query(DBModule).filter(DBModule.module_code == module_to_add.module_code).first()

    if code_err is not None:
        raise Exception

    new_module = DBModule(
                        module_code=module_to_add.module_code,
                        module_name=module_to_add.module_name,
                        module_location=module_to_add.module_location,
                        module_status=1)

    db.add(new_module)
    db.commit()

    return new_module


def get_module_by_code(db: Session, module_code: str):
    module = db.query(DBModule).filter(DBModule.module_code == module_code).first()

    if module is None:
        raise Exception

    return module


def update_module_by_index(db: Session, module_code: str, updated_module: ModuleUpdate):
    module_to_update: DBModule = db.query(DBModule).filter(DBModule.module_code == module_code).first()

    if module_to_update is None:
        raise Exception

    if updated_module.module_name is not None:
        module_to_update.module_name = updated_module.module_name
    if updated_module.module_location is not None:
        module_to_update.module_location = updated_module.module_location
    if updated_module.module_status is not None:
        module_to_update.module_status = updated_module.module_status

    db.commit()

    return module_to_update


def unwrap_rssi(db: Session, module_code: str, rssi: float, timestamp: str):
    module = db.query(DBModule).filter(DBModule.module_code == module_code).first()

    if module is None:
        raise Exception

    module.signal_power = rssi
    module.last_received_signal_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    db.commit()
    return module
