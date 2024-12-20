from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .estado_solicitud_modelos import EstadoSolicitudCreate, EstadoSolicitudResponse, EstadoSolicitudUpdate
from database.db_config import get_db_anserma
from .estado_solicitud_servicio import (
    get_estado_solicitudes,
    create_estado_solicitud,
    update_estado_solicitud,
    delete_estado_solicitud,
)

router = APIRouter()

@router.get("/estado_solicitudes/", response_model=List[EstadoSolicitudResponse])
async def read_estado_solicitudes(db: AsyncSession = Depends(get_db_anserma)):
    try:
        estado_solicitudes = await get_estado_solicitudes(db)
        return estado_solicitudes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estados de solicitud: {str(e)}"
        )

@router.post("/estado_solicitudes/", response_model=EstadoSolicitudResponse, status_code=status.HTTP_201_CREATED)
async def create_estado_solicitud_endpoint(
    estado_solicitud: EstadoSolicitudCreate, db: AsyncSession = Depends(get_db_anserma)
):
    try:
        estado_solicitud_dict = estado_solicitud.model_dump()
        nuevo_estado_solicitud = await create_estado_solicitud(db, estado_solicitud_dict)
        return nuevo_estado_solicitud
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear estado de solicitud: {str(e)}"
        )

@router.put("/estado_solicitudes/{estado_solicitud_id}", response_model=EstadoSolicitudResponse)
async def update_estado_solicitud_endpoint(
    estado_solicitud_id: int, 
    estado_solicitud: EstadoSolicitudUpdate, 
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        updated_estado_solicitud = await update_estado_solicitud(db, estado_solicitud_id, estado_solicitud)
        if not updated_estado_solicitud:
            raise HTTPException(status_code=404, detail="Estado de solicitud no encontrado")
        return updated_estado_solicitud
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar estado de solicitud: {str(e)}"
        )

@router.delete("/estado_solicitudes/{estado_solicitud_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estado_solicitud_endpoint(estado_solicitud_id: int, db: AsyncSession = Depends(get_db_anserma)):
    try:
        deleted = await delete_estado_solicitud(db, estado_solicitud_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Estado de solicitud no encontrado")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar estado de solicitud: {str(e)}"
        )
