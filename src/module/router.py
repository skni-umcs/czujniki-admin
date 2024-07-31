from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.dependecies import get_db
from .connector import get_all_modules, create_new_module, update_module_by_index, get_module_by_index
from .schemas import Module, ModuleCreate, ModuleUpdate
from src.auth.security import get_current_user

api_router = APIRouter(prefix="/module", tags=["module"])


@api_router.get("/", response_model=list[Module])
async def get_modules(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_all_modules(db)


@api_router.post("/", response_model=Module)
async def add_module(new_module: ModuleCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        created_module = create_new_module(db, new_module)

    except Exception as e:
        raise HTTPException(404, str(e))

    return created_module


@api_router.get("/{module_index}", response_model=Module)
async def get_module(module_index: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        module = get_module_by_index(db, module_index)
    except Exception as e:
        raise HTTPException(404, str(e))

    return module


@api_router.put("/{module_index}", response_model=Module)
async def update_module(module_index: int, updated_module: ModuleUpdate, db: Session = Depends(get_db),
                        current_user=Depends(get_current_user)):
    try:
        module_after_update = update_module_by_index(db, module_index, updated_module)
    except Exception as e:
        raise HTTPException(404, str(e))

    return module_after_update
