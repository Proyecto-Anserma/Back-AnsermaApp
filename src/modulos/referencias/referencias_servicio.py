from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

async def get_referencia(tabla, db: AsyncSession):
    """
    Función genérica para obtener datos de una tabla.
    :param tabla: Modelo de la tabla (ej. TipoSolicitud, Genero, etc.)
    :param db: Sesión de base de datos
    """
    try:
        result = await db.execute(select(tabla))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")
