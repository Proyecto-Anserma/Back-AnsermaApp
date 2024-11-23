from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .solicitud_modelos import SolicitudCreate, SolicitudResponse, SolicitudUpdate, SolicitudFiltrar
from database.db_config import get_db_anserma
from .solicitud_servicio import *

router = APIRouter()

'''Consultar todas las solicitudes'''
@router.get("/consultar-solicitudes/", response_model=List[SolicitudResponse])
async def read_solicitudes(db: AsyncSession = Depends(get_db_anserma)):
    try:
        solicitudes = await get_solicitudes(db)
        return solicitudes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener solicitudes: {str(e)}"
        )
        
@router.post("/filtrar-solicitudes/", response_model=List[SolicitudResponse])
async def filtrar_solicitudes_endpoint(
    filtros: SolicitudFiltrar = Body(...),
    db: AsyncSession = Depends(get_db_anserma)
):
    """
    Filtra solicitudes por descripción o id_ciudadano_solicitud.
    Si no se envían filtros, devuelve todas las solicitudes.
    """
    try:
        solicitudes = await filtrar_solicitudes(db, filtros)
        return solicitudes
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al filtrar solicitudes: {str(e)}"
        )


''' Crear solicitud'''
@router.post("/crear-solicitud/", response_model=SolicitudResponse, status_code=status.HTTP_201_CREATED)
async def create_solicitud_endpoint(solicitud: SolicitudCreate, db: AsyncSession = Depends(get_db_anserma)):
    try:
        solicitud_dict = solicitud.model_dump()
        nueva_solicitud = await create_solicitud(db, solicitud_dict)
        return nueva_solicitud
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear solicitud: {str(e)}"
        )

''' Editar solicitud'''
@router.put("/editar-solicitud/{solicitud_id}", response_model=SolicitudResponse)
async def update_solicitud_endpoint(
    solicitud_id: int, 
    solicitud: SolicitudUpdate, 
    db: AsyncSession = Depends(get_db_anserma)
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

'''Eliminar solicitud'''
@router.delete("/eliminar-solicitud/{solicitud_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solicitud_endpoint(solicitud_id: int, db: AsyncSession = Depends(get_db_anserma)):
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


