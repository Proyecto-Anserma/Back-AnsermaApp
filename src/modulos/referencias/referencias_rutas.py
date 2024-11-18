from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .referencias_servicio import get_referencia
from .referencias_db_modelo import TipoSolicitud, Genero, TipoUbicacion, PertenenciaEtnica, Rol, Estado
from database.db_config import get_db_anserma, get_db_usuarios

router = APIRouter(prefix="/referencias")

# Rutas relacionadas con la base de datos de Anserma
@router.get("/tipo_solicitudes/")
async def read_tipo_solicitudes(db: AsyncSession = Depends(get_db_anserma)):
    return await get_referencia(TipoSolicitud, db)

@router.get("/tipo_ubicaciones/")
async def read_tipo_ubicaciones(db: AsyncSession = Depends(get_db_anserma)):
    return await get_referencia(TipoUbicacion, db)

@router.get("/generos/")
async def read_generos(db: AsyncSession = Depends(get_db_anserma)):
    return await get_referencia(Genero, db)

@router.get("/pertenencia_etnica/")
async def read_pertenencia_etnica(db: AsyncSession = Depends(get_db_anserma)):
    return await get_referencia(PertenenciaEtnica, db)

@router.get("/estados/")
async def read_estados(db: AsyncSession = Depends(get_db_anserma)):
    return await get_referencia(Estado, db)

@router.get("/rol/")
async def read_rol(db: AsyncSession = Depends(get_db_usuarios)):
    return await get_referencia(Rol, db)
