from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.security import get_current_user
from .schemas import User

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=User)
def read_users_me(current_user: User  = Depends(get_current_user)):
    return current_user