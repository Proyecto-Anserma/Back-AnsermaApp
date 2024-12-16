from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.db_config import get_db_anserma
from .estado_modelos import EstadoResponse
from .estado_servicio import get_estados

router = APIRouter()

@router.get("/estados/", response_model=List[EstadoResponse])
async def get_estados_endpoint(db: AsyncSession = Depends(get_db_anserma)):
    try:
        estados = await get_estados(db)
        return estados
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al obtener estados: {str(e)}"
        )
