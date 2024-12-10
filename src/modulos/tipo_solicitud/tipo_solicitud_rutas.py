from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.elements import WKTElement
from typing import List
from shapely import wkt
from database.db_config import get_db_anserma
from .tipo_solicitud_modelos import PertenenciaEtnica
from .tipo_solicitud_servicio import *

router = APIRouter()

@router.get("/obtener_todos/", response_model=List[PertenenciaEtnica])
async def obtener_todos(db: AsyncSession = Depends(get_db_anserma)):
    try:
        tipo_solicitudes = await get_tipo_solicitud(db)
        return tipo_solicitudes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener todos los tipos de solicitud: {str(e)}"
        )