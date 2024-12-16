from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .cantidad_origen_ayuda_modelos import CantidadOrigenAyudaCreate, CantidadOrigenAyudaResponse
from database.db_config import get_db_anserma
from .cantidad_origen_ayuda_servicio import (
    get_cantidades_origen_ayuda, 
    create_cantidad_origen_ayuda, 
    update_cantidad_origen_ayuda, 
    delete_cantidad_origen_ayuda
)

router = APIRouter()

@router.get("/cantidades_origen_ayuda/", response_model=List[CantidadOrigenAyudaResponse])
async def read_cantidades_origen_ayuda(db: AsyncSession = Depends(get_db_anserma)):
    try:
        cantidades = await get_cantidades_origen_ayuda(db)
        return cantidades
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener cantidades de origen de ayuda: {str(e)}"
        )

@router.post("/crear_cantidades_origen_ayuda/", response_model=CantidadOrigenAyudaResponse, status_code=status.HTTP_201_CREATED)
async def create_cantidad_origen_ayuda_endpoint(
    cantidad_origen_ayuda: CantidadOrigenAyudaCreate, 
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        nueva_cantidad = await create_cantidad_origen_ayuda(db, cantidad_origen_ayuda)
        return nueva_cantidad
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear cantidad de origen de ayuda: {str(e)}"
        )
        

@router.put(
    "/cantidades_origen_ayuda/{cantidad_origen_ayuda_id}",
    response_model=CantidadOrigenAyudaResponse,
    status_code=status.HTTP_200_OK
)
async def update_cantidad_origen_ayuda_endpoint(
    cantidad_origen_ayuda_id: int,
    cantidad_origen_ayuda: CantidadOrigenAyudaCreate,
    db: AsyncSession = Depends(get_db_anserma)
):
    """
    Actualiza una cantidad de origen de ayuda existente.

    :param cantidad_origen_ayuda_id: ID de la cantidad de origen de ayuda a actualizar
    :param cantidad_origen_ayuda: Datos nuevos para actualizar
    :param db: Sesión de base de datos
    :return: La cantidad de origen de ayuda actualizada o un error HTTP
    """
    try:
        updated_cantidad = await update_cantidad_origen_ayuda(
            db, cantidad_origen_ayuda_id, cantidad_origen_ayuda
        )
        if not updated_cantidad:
            raise HTTPException(
                status_code=404,
                detail="Cantidad de origen de ayuda no encontrada"
            )
        return updated_cantidad
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar cantidad de origen de ayuda: {str(e)}"
        )


@router.delete("/cantidades_origen_ayuda/{cantidad_origen_ayuda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cantidad_origen_ayuda_endpoint(
    cantidad_origen_ayuda_id: int, 
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        deleted = await delete_cantidad_origen_ayuda(db, cantidad_origen_ayuda_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Cantidad de origen de ayuda no encontrada")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar cantidad de origen de ayuda: {str(e)}"
        )