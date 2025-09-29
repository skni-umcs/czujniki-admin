from fastapi import APIRouter, Depends, HTTPException, status

from .schemas import User

router = APIRouter(prefix="/user", tags=["user"])
