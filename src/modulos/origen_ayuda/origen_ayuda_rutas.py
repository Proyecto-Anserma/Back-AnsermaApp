from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .origen_ayuda_modelos import OrigenAyudaCreate, OrigenAyudaResponse
from database.db_config import get_db_anserma
from .origen_ayuda_servicio import get_origenes_ayuda, create_origen_ayuda, delete_origen_ayuda

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