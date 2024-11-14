from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .ubicacion_servicio import get_ubicaciones
from database.db import get_db

router = APIRouter(prefix="/ubicaciones")

@router.get("/ubicaciones/")
async def read_ubicaciones(db: AsyncSession = Depends(get_db)):
    return await get_ubicaciones(db)