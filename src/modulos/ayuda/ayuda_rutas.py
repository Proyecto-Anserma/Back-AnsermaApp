from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .ayuda_modelos import AyudaCreate, AyudaResponse
from database.db_config import get_db_anserma
from .ayuda_servicio import get_ayudas, create_ayuda, delete_ayuda

router = APIRouter()

@router.get("/ayudas/", response_model=List[AyudaResponse])
async def read_ayudas(db: AsyncSession = Depends(get_db_anserma)):
    try:
        ayudas = await get_ayudas(db)
        return ayudas
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener ayudas: {str(e)}"
        )

@router.post("/ayudas/", response_model=AyudaResponse, status_code=status.HTTP_201_CREATED)
async def create_ayuda_endpoint(ayuda: AyudaCreate, db: AsyncSession = Depends(get_db_anserma)):
    try:
        nueva_ayuda = await create_ayuda(db, ayuda)
        return nueva_ayuda
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear ayuda: {str(e)}"
        )

@router.delete("/ayudas/{ayuda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ayuda_endpoint(ayuda_id: int, db: AsyncSession = Depends(get_db_anserma)):
    try:
        deleted = await delete_ayuda(db, ayuda_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Ayuda no encontrada")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar ayuda: {str(e)}"
        )
