from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .solicitud_modelos import SolicitudCreate, SolicitudResponse, SolicitudUpdate
from database.db import get_db
from .solicitud_servicio import (
    get_solicitudes,
    create_solicitud,
    update_solicitud,
    delete_solicitud,
)

router = APIRouter()

@router.get("/solicitudes/", response_model=List[SolicitudResponse])
async def read_solicitudes(db: AsyncSession = Depends(get_db)):
    try:
        solicitudes = await get_solicitudes(db)
        return solicitudes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener solicitudes: {str(e)}"
        )

@router.post("/solicitudes/", response_model=SolicitudResponse, status_code=status.HTTP_201_CREATED)
async def create_solicitud_endpoint(solicitud: SolicitudCreate, db: AsyncSession = Depends(get_db)):
    try:
        solicitud_dict = solicitud.model_dump()
        nueva_solicitud = await create_solicitud(db, solicitud_dict)
        return nueva_solicitud
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear solicitud: {str(e)}"
        )

@router.put("/solicitudes/{solicitud_id}", response_model=SolicitudResponse)
async def update_solicitud_endpoint(
    solicitud_id: int, 
    solicitud: SolicitudUpdate, 
    db: AsyncSession = Depends(get_db)
):
    try:
        updated_solicitud = await update_solicitud(db, solicitud_id, solicitud)
        if not updated_solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return updated_solicitud
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar solicitud: {str(e)}"
        )

@router.delete("/solicitudes/{solicitud_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solicitud_endpoint(solicitud_id: int, db: AsyncSession = Depends(get_db)):
    try:
        deleted = await delete_solicitud(db, solicitud_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar solicitud: {str(e)}"
        )


