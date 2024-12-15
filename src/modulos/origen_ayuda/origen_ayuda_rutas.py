from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .origen_ayuda_modelos import OrigenAyudaCreate, OrigenAyudaResponse, OrigenAyudaFiltro
from database.db_config import get_db_anserma
from .origen_ayuda_servicio import get_origenes_ayuda, create_origen_ayuda, update_origen_ayuda,delete_origen_ayuda, filtrar_origen_ayuda_por_nit

router = APIRouter()

@router.get("/origenes-ayuda/", response_model=List[OrigenAyudaResponse])
async def read_origenes_ayuda(db: AsyncSession = Depends(get_db_anserma)):
    try:
        origenes_ayuda = await get_origenes_ayuda(db)
        return origenes_ayuda
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener orígenes de ayuda: {str(e)}"
        )

@router.post("/origenes-ayuda/", response_model=OrigenAyudaResponse, status_code=status.HTTP_201_CREATED)
async def create_origen_ayuda_endpoint(
    origen_ayuda: OrigenAyudaCreate, 
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        nuevo_origen_ayuda = await create_origen_ayuda(db, origen_ayuda)
        return nuevo_origen_ayuda
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear origen de ayuda: {str(e)}"
        )


@router.put(
    "/origenes-ayuda/{origen_ayuda_id}",
    response_model=OrigenAyudaResponse, status_code=status.HTTP_200_OK)
async def update_origen_ayuda_endpoint(
    origen_ayuda_id: int,
    origen_ayuda: OrigenAyudaCreate,
    db: AsyncSession = Depends(get_db_anserma)
):
    """
    Actualiza un origen de ayuda existente.

    :param origen_ayuda_id: ID del origen de ayuda a actualizar
    :param origen_ayuda: Datos nuevos para actualizar
    :param db: Sesión de base de datos
    :return: El origen de ayuda actualizado o un error HTTP
    """
    try:
        updated_origen = await update_origen_ayuda(db, origen_ayuda_id, origen_ayuda)
        if not updated_origen:
            raise HTTPException(
                status_code=404,
                detail="Origen de ayuda no encontrado"
            )
        return updated_origen
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar origen de ayuda: {str(e)}"
        )


@router.delete("/origenes-ayuda/{origen_ayuda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_origen_ayuda_endpoint(
    origen_ayuda_id: int, 
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        deleted = await delete_origen_ayuda(db, origen_ayuda_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Origen de ayuda no encontrado")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar origen de ayuda: {str(e)}"
        )

@router.post("/filtrar/", response_model=List[OrigenAyudaResponse])
async def filtrar_origen_ayuda_endpoint(
    filtros: OrigenAyudaFiltro = Body(...),
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        origenes = await filtrar_origen_ayuda_por_nit(db, filtros.nit)
        return origenes
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al filtrar origen ayuda: {str(e)}"
        )