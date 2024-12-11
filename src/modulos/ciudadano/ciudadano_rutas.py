from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .ciudadano_modelos import CiudadanoCreate, CiudadanoResponse, CiudadanoBase, CiudadanoFiltrar
from database.db_config import get_db_anserma
from .ciudadano_servicio import *

router = APIRouter()

@router.post("/crear-ciudadano/", response_model=CiudadanoResponse, status_code=status.HTTP_201_CREATED)
async def create_ciudadano_endpoint(ciudadano: CiudadanoCreate, db: AsyncSession = Depends(get_db_anserma)):
    try:
        ciudadano_dict = ciudadano.model_dump()
        nuevo_ciudadano = await create_ciudadano(db, ciudadano_dict)
        return nuevo_ciudadano
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear ciudadano: {str(e)}"
        )

@router.put("/editar-ciudadano/{ciudadano_id}", response_model=CiudadanoResponse)
async def update_ciudadano_endpoint(
    ciudadano_id: str, 
    ciudadano: CiudadanoCreate, 
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
            detail=f"Error al actualizar ciudadano: {str(e)}"
        )

@router.post("/filtrar-ciudadanos/", response_model=List[CiudadanoResponse])
async def filtrar_ciudadanos_endpoint(
    filtros: CiudadanoFiltrar = Body(...),
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        ciudadanos = await filtrar_ciudadanos(db, filtros)
        return ciudadanos
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al filtrar ciudadanos: {str(e)}"
        )

# Eliminar ciudadano
@router.delete("/eliminar-ciudadano/{ciudadano_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ciudadano_endpoint(ciudadano_id: int, db: AsyncSession = Depends(get_db_anserma)):
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