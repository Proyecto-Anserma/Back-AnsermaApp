from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .ubicacion_modelos import UbicacionCreate, UbicacionUpdate
from database.db_config import get_db_anserma, get_db_usuarios
from .ubicacion_servicio import (
    get_ubicaciones,
    create_ubicacion,
    update_ubicacion,
    delete_ubicacion
)

router = APIRouter(prefix="/ubicaciones")

@router.get("/")
async def read_ubicaciones(source: str, db: AsyncSession = Depends(get_db_anserma)):
    """
    source: Indica la base de datos a usar (anserma o usuarios).
    """
    if source == "usuarios":
        db = Depends(get_db_usuarios)
    return await get_ubicaciones(db)

@router.post("/", response_model=UbicacionCreate)
async def create_ubicacion_endpoint(
    source: str, ubicacion_data: UbicacionCreate, db: AsyncSession = Depends(get_db_anserma)
):
    if source == "usuarios":
        db = Depends(get_db_usuarios)
    return await create_ubicacion(db, ubicacion_data)

@router.put("/{ubicacion_id}", response_model=UbicacionUpdate)
async def update_ubicacion_endpoint(
    source: str, ubicacion_id: int, ubicacion_data: UbicacionUpdate, db: AsyncSession = Depends(get_db_anserma)
):
    if source == "usuarios":
        db = Depends(get_db_usuarios)
    ubicacion_actualizada = await update_ubicacion(db, ubicacion_id, ubicacion_data)
    if ubicacion_actualizada is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return ubicacion_actualizada

@router.delete("/{ubicacion_id}")
async def delete_ubicacion_endpoint(
    source: str, ubicacion_id: int, db: AsyncSession = Depends(get_db_anserma)
):
    if source == "usuarios":
        db = Depends(get_db_usuarios)
    deleted = await delete_ubicacion(db, ubicacion_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return {"detail": "Ubicación eliminada correctamente"}
