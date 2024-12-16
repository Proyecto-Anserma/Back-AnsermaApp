from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
from sqlalchemy.orm import selectinload
from .ayuda_db_modelo import Ayuda
from .ayuda_modelos import AyudaCreate, AyudasFiltrar
from src.modulos.cantidad_origen_ayuda.cantidad_origen_ayuda_db_modelo import CantidadOrigenAyuda


async def get_ayudas(db: AsyncSession):
    try:
        query = (
            select(Ayuda)
            .options(selectinload(Ayuda.solicitudes_ayuda))
            .options(
                selectinload(Ayuda.cantidades_origen_ayuda)
                .selectinload(CantidadOrigenAyuda.origen_ayuda)
            )
        )
        result = await db.execute(query)
        return result.unique().scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener ayudas: {str(e)}")

async def create_ayuda(db: AsyncSession, ayuda_data: AyudaCreate):
    try:
        nueva_ayuda = Ayuda(**ayuda_data.model_dump())
        db.add(nueva_ayuda)
        await db.commit()
        
        await db.execute(
            text("SELECT setval('ayuda_id_ayuda_seq', (SELECT MAX(id_ayuda) FROM ayuda))")
        )
        
        # Cargamos la ayuda creada con sus relaciones
        query = (
            select(Ayuda)
            .options(selectinload(Ayuda.solicitudes_ayuda))
            .options(selectinload(Ayuda.cantidades_origen_ayuda))
            .where(Ayuda.id_ayuda == nueva_ayuda.id_ayuda)
        )
        result = await db.execute(query)
        nueva_ayuda_con_relaciones = result.unique().scalar_one_or_none()
        
        return nueva_ayuda_con_relaciones
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear ayuda: {str(e)}")
    

async def update_ayuda(db: AsyncSession, ayuda_id: int, ayuda_data: AyudaCreate):
    """
    Actualiza una ayuda existente.

    :param db: Sesión de base de datos
    :param ayuda_id: ID de la ayuda a actualizar
    :param ayuda_data: Datos de la ayuda a actualizar
    :return: La ayuda actualizada o None si no se encuentra
    """
    try:
        # Primero actualizamos los datos
        result = await db.execute(
            sql_update(Ayuda)
            .where(Ayuda.id_ayuda == ayuda_id)
            .values(**ayuda_data.model_dump())
            .returning(Ayuda)
        )
        updated_ayuda = result.scalar_one_or_none()
        
        if updated_ayuda:
            await db.commit()
            
            # Cargamos la ayuda actualizada con sus relaciones
            query = (
                select(Ayuda)
                .options(selectinload(Ayuda.solicitudes_ayuda))
                .options(selectinload(Ayuda.cantidades_origen_ayuda))
                .where(Ayuda.id_ayuda == ayuda_id)
            )
            result = await db.execute(query)
            updated_ayuda = result.unique().scalar_one_or_none()
            
        return updated_ayuda
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar ayuda: {str(e)}")
    

async def delete_ayuda(db: AsyncSession, ayuda_id: int):
    try:
        result = await db.execute(
            sql_delete(Ayuda)
            .where(Ayuda.id_ayuda == ayuda_id)
            .returning(Ayuda.id_ayuda)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar ayuda: {str(e)}")


async def filtrar_ayudas(db: AsyncSession, filtros: AyudasFiltrar):
    try:
        query = (
            select(Ayuda)
            .options(selectinload(Ayuda.solicitudes_ayuda))
            .options(
                selectinload(Ayuda.cantidades_origen_ayuda)
                .selectinload(CantidadOrigenAyuda.origen_ayuda)
            )
        )

        if filtros.fecha_creacion_ayuda:
            query = query.where(Ayuda.fecha_creacion_ayuda == filtros.fecha_creacion_ayuda)

        result = await db.execute(query)
        return result.unique().scalars().all()
    except Exception as e:
        raise Exception(f"Error al filtrar ayudas: {str(e)}")      