from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .solicitud_servicio import get_solicitudes
from database.db import get_db

router = APIRouter()

@router.get("/solicitudes/")
async def read_solicitudes(db: AsyncSession = Depends(get_db)):
    return await get_solicitudes(db)
