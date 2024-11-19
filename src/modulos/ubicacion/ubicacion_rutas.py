from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .ubicacion_modelos import UbicacionCreate, UbicacionUpdate, UbicacionBase
from .ubicacion_servicio import get_ubicaciones, create_ubicacion, update_ubicacion, delete_ubicacion
from database.db_config import get_db_anserma

router = APIRouter()

@router.get("/ubicaciones/", response_model=List[UbicacionBase])
async def read_ubicaciones(db: AsyncSession = Depends(get_db_anserma)):
    """
    Obtiene todas las ubicaciones.
    """
    try:
        ubicaciones = await get_ubicaciones(db)
        return ubicaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicaciones: {str(e)}"
        )

@router.post("/ubicaciones/", response_model=UbicacionBase, status_code=status.HTTP_201_CREATED)
async def create_ubicacion_endpoint(
    ubicacion_data: UbicacionCreate,
    db: AsyncSession = Depends(get_db_anserma)
):
    """
    Crea una nueva ubicación.
    """
    try:
        nueva_ubicacion = await create_ubicacion(db, ubicacion_data)
        return nueva_ubicacion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear ubicación: {str(e)}"
        )

@router.put("/ubicaciones/{ubicacion_id}", response_model=UbicacionBase, status_code=status.HTTP_200_OK)
async def update_ubicacion_endpoint(
    ubicacion_id: int,
    ubicacion_data: UbicacionUpdate,
    db: AsyncSession = Depends(get_db_anserma)
):
    """
    Actualiza una ubicación existente.
    """
    try:
        ubicacion_actualizada = await update_ubicacion(db, ubicacion_id, ubicacion_data)
        if not ubicacion_actualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ubicación no encontrada"
            )
        return ubicacion_actualizada
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar ubicación: {str(e)}"
        )

@router.delete("/ubicaciones/{ubicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ubicacion_endpoint(
    ubicacion_id: int,
    db: AsyncSession = Depends(get_db_anserma)
):
    """
    Elimina una ubicación por su ID.
    """
    try:
        deleted = await delete_ubicacion(db, ubicacion_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ubicación no encontrada"
            )
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar ubicación: {str(e)}"
        )
