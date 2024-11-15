from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .ubicacion_modelos import UbicacionCreate, UbicacionUpdate
from database.db import get_db
from .ubicacion_servicio import (
    get_ubicaciones,
    create_ubicacion,
    update_ubicacion,
    delete_ubicacion
)

router = APIRouter(prefix="/ubicaciones")

@router.get("/ubicaciones/")
async def read_ubicaciones(db: AsyncSession = Depends(get_db)):
    return await get_ubicaciones(db)

@router.post("/ubicaciones/", response_model=UbicacionCreate)
async def create_ubicacion_endpoint(ubicacion_data: UbicacionCreate, db: AsyncSession = Depends(get_db)):
    return await create_ubicacion(db, ubicacion_data)

@router.put("/ubicaciones/{ubicacion_id}", response_model=UbicacionUpdate)
async def update_ubicacion_endpoint(ubicacion_id: int, ubicacion_data: UbicacionUpdate, db: AsyncSession = Depends(get_db)):
    ubicacion_actualizada = await update_ubicacion(db, ubicacion_id, ubicacion_data)
    if ubicacion_actualizada is None:
        raise HTTPException(status_code=404, detail="ubicacion no encontrada")
    return ubicacion_actualizada

@router.delete("/ubicaciones/{ubicacion_id}")
async def delete_ubicacion_endpoint(ubicacion_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_ubicacion(db, ubicacion_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ubicacion no encontrada")
    return {"detail": "ubicacion eliminada correctamente"}