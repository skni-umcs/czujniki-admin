from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.dependecies import get_db
from .connector import get_all_modules, create_new_module, update_module_by_index, get_module_by_code, unwrap_rssi
from .schemas import Module, ModuleCreate, ModuleUpdate, RSSIData
from src.auth.security import get_current_user

api_router = APIRouter(prefix="/module", tags=["module"])


@api_router.get("/", response_model=list[Module])
async def get_modules(db: Session = Depends(get_db),):
    return get_all_modules(db)


@api_router.post("/", response_model=Module)
async def add_module(new_module: ModuleCreate, db: Session = Depends(get_db), ):
    try:
        created_module = create_new_module(db, new_module)

    except Exception as e:
        raise HTTPException(404, str(e))

    return created_module


@api_router.post("/receive_rssi")
async def receive_rssi(rssi_data: RSSIData, db: Session = Depends(get_db), ):
    try:
        unwrap_rssi(db, rssi_data.module_code, rssi_data.rssi, rssi_data.timestamp)
    except Exception as e:
        raise HTTPException(404, str(e))

    return {"message": "RSSI data received"}


@api_router.get("/{module_code}", response_model=Module)
async def get_module(module_code: str, db: Session = Depends(get_db), ):
    try:
        module = get_module_by_code(db, module_code)
    except Exception as e:
        raise HTTPException(404, str(e))

    return module


@api_router.put("/{module_code}", response_model=Module)
async def update_module(module_code: str, updated_module: ModuleUpdate, db: Session = Depends(get_db),
                        ):
    try:
        module_after_update = update_module_by_index(db, module_code, updated_module)
    except Exception as e:
        raise HTTPException(404, str(e))

    return module_after_update
