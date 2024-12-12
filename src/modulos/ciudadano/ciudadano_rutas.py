from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.elements import WKTElement
from typing import List
from shapely import wkt
from .ciudadano_modelos import CiudadanoCreate, CiudadanosFiltrar, Ciudadano
from database.db_config import get_db_anserma
from .ciudadano_servicio import (
    get_ciudadanos,
    create_ciudadano,
    update_ciudadano,
    delete_ciudadano,
    filtrar_ciudadanos
)

router = APIRouter()

@router.get("/ciudadanos/", response_model=List[Ciudadano])
async def read_ciudadanos(db: AsyncSession = Depends(get_db_anserma)):
    try:
        ciudadanos = await get_ciudadanos(db)
        return ciudadanos
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener ciudadanos: {str(e)}"
        )


@router.post("/ciudadanos/", response_model=Ciudadano, status_code=status.HTTP_201_CREATED)
async def create_ciudadano_endpoint(ciudadano: CiudadanoCreate, db: AsyncSession = Depends(get_db_anserma)):
    try:
        ciudadano_dict = ciudadano.model_dump()
        ciudadano_dict['telefono_ciudadano'] = int(ciudadano_dict['telefono_ciudadano'])
        nuevo_ciudadano = await create_ciudadano(db, ciudadano_dict)
        return nuevo_ciudadano
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear ciudadano: {str(e)}"
        )
        
        
@router.put("/editar-ciudadano/{ciudadano_id}", response_model=None)
async def update_ciudadano_endpoint(
    ciudadano_id: str, 
    ciudadano: CiudadanoCreate,  # Cambiar a SolicitudCreate en lugar de SolicitudBase
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        updated_ciudadano = await update_ciudadano(db, ciudadano_id, ciudadano)
        if not updated_ciudadano:
            raise HTTPException(status_code=404, detail="Ciudadano no encontrado")
        return updated_ciudadano
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar solicitud: {str(e)}"
        )
        

@router.delete("/ciudadanos/{ciudadano_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ciudadano_endpoint(ciudadano_id: str, db: AsyncSession = Depends(get_db_anserma)):
    try:
        deleted = await delete_ciudadano(db, ciudadano_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Ciudadano no encontrado")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar ciudadano: {str(e)}"
        )
    
@router.post("/filtrar-ciudadanos/", response_model=List[Ciudadano])
async def filtrar_ciudadanos_endpoint(
    filtros: CiudadanosFiltrar = Body(...),
    db: AsyncSession = Depends(get_db_anserma)
):
    """
    Filtra ciudadanos por cedula.
    Si no se envían filtros, devuelve todas los ciudadanos.
    """
    try:
        ciudadanos = await filtrar_ciudadanos(db, filtros)
        return ciudadanos
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al filtrar ciudadanos: {str(e)}"
        )