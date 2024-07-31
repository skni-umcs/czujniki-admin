from .models import DBModule
from sqlalchemy.orm import Session
from .schemas import ModuleCreate, ModuleUpdate


def get_all_modules(db: Session) -> list[DBModule]:
    modules = db.query(DBModule).all()
    return modules


def create_new_module(db: Session,
                      module_to_add: ModuleCreate
                      ) -> DBModule:

    code_err = db.query(DBModule).filter(DBModule.module_code == module_to_add.module_code).first()

    if code_err is not None:
        raise Exception

    new_module = DBModule(
                        module_name=module_to_add.module_name,
                        module_code=module_to_add.module_code,
                        location=module_to_add.location,
                        is_active=module_to_add.is_active,
                        is_deleted=0,
                        signal_power=0,
                        url=module_to_add.url
                        )

    db.add(new_module)
    db.commit()

    return new_module


def get_module_by_index(db: Session, module_index: int):
    module = db.query(DBModule).filter(DBModule.module_id == module_index).first()

    if module is None:
        raise Exception

    return module


def update_module_by_index(db: Session, module_index: int, updated_module: ModuleUpdate):
    module_to_update: DBModule = db.query(DBModule).filter(DBModule.module_id == module_index).first()

    if module_to_update is None:
        raise Exception

    if updated_module.module_code is not None:
        module_to_update.module_code = updated_module.module_code
    if updated_module.module_name is not None:
        module_to_update.module_name = updated_module.module_name
    if updated_module.location is not None:
        module_to_update.location = updated_module.location
    if updated_module.is_active is not None:
        module_to_update.is_active = updated_module.is_active
    if updated_module.is_deleted is not None:
        module_to_update.is_deleted = updated_module.is_deleted
    if updated_module.signal_power is not None:
        module_to_update.signal_power = updated_module.signal_power
    if updated_module.url is not None:
        module_to_update.url = updated_module.url

    db.commit()

    return module_to_update
