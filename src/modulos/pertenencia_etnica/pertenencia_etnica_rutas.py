from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.elements import WKTElement
from typing import List
from shapely import wkt
from database.db_config import get_db_anserma
from .pertenencia_etnica_modelos import PertenenciaEtnica
from .pertenencia_etnica_servicio import *

router = APIRouter()

@router.get("/obtener_todos/", response_model=None)
async def obtener_todos(db: AsyncSession = Depends(get_db_anserma)):
    try:
        pertenencias_etnicas = await get_pertenencia_etnica(db)
        return pertenencias_etnicas
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener todas las pertenencias etnicas: {str(e)}"
        )