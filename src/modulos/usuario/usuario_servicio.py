from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text, update as sql_update, delete as sql_delete
from .usuario_db_modelo import Usuario
from .usuario_modelos import UsuarioUpdate

async def get_usuarios(db: AsyncSession):
    try:
        result = await db.execute(select(Usuario))
        return result.scalars().all()
    except Exception as e:
        raise Exception(f"Error al obtener usuarios: {str(e)}")


async def create_usuario(db: AsyncSession, usuario_data: dict):
    try:
        nuevo_usuario = Usuario(**usuario_data)
        db.add(nuevo_usuario)
        await db.commit()
        
        # Ajustamos el valor de la secuencia si es necesario (si estás usando secuencias en la base de datos)
        await db.execute(
            text("SELECT setval('usuario_numero_identificacion_usuario_seq', (SELECT MAX(numero_identificacion_usuario) FROM usuario))")
        )
        await db.refresh(nuevo_usuario)
        return nuevo_usuario
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al crear usuario: {str(e)}")


async def update_usuario(db: AsyncSession, usuario_id: str, usuario_data: UsuarioUpdate):
    try:
        # Busca el usuario por el identificador
        result = await db.execute(select(Usuario).where(Usuario.numero_identificacion_usuario == usuario_id))
        usuario = result.scalar_one_or_none()
        if usuario is None:
            return None

        # Actualiza el usuario con los datos proporcionados
        update_data = usuario_data.dict(exclude_unset=True)
        await db.execute(
            sql_update(Usuario)
            .where(Usuario.numero_identificacion_usuario == usuario_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(usuario)
        return usuario
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al actualizar usuario: {str(e)}")


async def delete_usuario(db: AsyncSession, usuario_id: str):
    try:
        result = await db.execute(
            sql_delete(Usuario)
            .where(Usuario.numero_identificacion_usuario == usuario_id)
            .returning(Usuario.numero_identificacion_usuario)
        )
        deleted = result.scalar_one_or_none()
        await db.commit()
        return deleted is not None
    except Exception as e:
        await db.rollback()
        raise Exception(f"Error al eliminar usuario: {str(e)}")
