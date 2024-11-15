from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .solicitud_modelos import SolicitudCreate, SolicitudUpdate
from database.db import get_db
from .solicitud_servicio import (
    get_solicitudes,
    create_solicitud,
    update_solicitud,
    delete_solicitud
)

router = APIRouter()

@router.get("/solicitudes/")
async def read_solicitudes(db: AsyncSession = Depends(get_db)):
    return await get_solicitudes(db)

@router.post("/solicitudes/", response_model=SolicitudCreate)
async def create_solicitud_endpoint(solicitud_data: SolicitudCreate, db: AsyncSession = Depends(get_db)):
    return await create_solicitud(db, solicitud_data)

@router.put("/solicitudes/{solicitud_id}", response_model=SolicitudUpdate)
async def update_solicitud_endpoint(solicitud_id: int, solicitud_data: SolicitudUpdate, db: AsyncSession = Depends(get_db)):
    solicitud_actualizada = await update_solicitud(db, solicitud_id, solicitud_data)
    if solicitud_actualizada is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud_actualizada

@router.delete("/solicitudes/{solicitud_id}")
async def delete_solicitud_endpoint(solicitud_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_solicitud(db, solicitud_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return {"detail": "Solicitud eliminada correctamente"}

