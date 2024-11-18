from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_config import get_db_usuarios
from .usuario_modelos import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from .usuario_servicio import get_usuarios, create_usuario, update_usuario, delete_usuario

router = APIRouter()

@router.get("/usuarios/", response_model=List[UsuarioResponse])
async def obtener_usuarios(db: AsyncSession = Depends(get_db_usuarios)):
    try:
        return await get_usuarios(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/usuarios/", response_model=UsuarioResponse)
async def crear_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db_usuarios)):
    try:
        return await create_usuario(db, usuario.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(usuario_id: str, usuario: UsuarioUpdate, db: AsyncSession = Depends(get_db_usuarios)):
    try:
        updated_usuario = await update_usuario(db, usuario_id, usuario)
        if updated_usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return updated_usuario
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/usuarios/{usuario_id}", response_model=bool)
async def eliminar_usuario(usuario_id: str, db: AsyncSession = Depends(get_db_usuarios)):
    try:
        result = await delete_usuario(db, usuario_id)
        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
