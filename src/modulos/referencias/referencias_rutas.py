from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .referencias_servicio import *
from database.db import get_db

router = APIRouter(prefix="/referencias")

@router.get("/tipo_solicitudes/")
async def read_tipo_solicitudes(db: AsyncSession = Depends(get_db)):
    return await get_tipo_solicitudes(db)

@router.get("/ubicaciones/")
async def read_ubicaciones(db: AsyncSession = Depends(get_db)):
    return await get_ubicaciones(db)

@router.get("/tipo_ubicaciones/")
async def read_tipo_ubicaciones(db: AsyncSession = Depends(get_db)):
    return await get_tipo_ubicaciones(db)

@router.get("/generos/")
async def read_generos(db: AsyncSession = Depends(get_db)):
    return await get_generos(db)

@router.get("/pertenencia_etnica/")
async def read_pertenencia_etnica(db: AsyncSession = Depends(get_db)):
    return await get_pertenencia_etnica(db)
