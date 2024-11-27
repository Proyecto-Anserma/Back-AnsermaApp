from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .ayuda_modelos import AyudaCreate, AyudaResponse
from database.db_config import get_db_anserma
from .ayuda_servicio import get_ayudas, create_ayuda, update_ayuda, delete_ayuda, filtrar_ayudas
from .ayuda_modelos import AyudasFiltrar


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

'''crear ayuda '''
@router.post("/crear-ayuda/", response_model=AyudaResponse, status_code=status.HTTP_201_CREATED)
async def create_ayuda_endpoint(ayuda: AyudaCreate, db: AsyncSession = Depends(get_db_anserma)):
    try:
        nueva_ayuda = await create_ayuda(db, ayuda)
        return nueva_ayuda 
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear ayuda: {str(e)}"
        )
    
@router.post("/filtrar-ayudas/", response_model=List[AyudaResponse])
async def filtrar_ayudas_endpoint(
    filtros: AyudasFiltrar = Body(...),
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        ayudas = await filtrar_ayudas(db, filtros)
        return ayudas   
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al filtrar ayudas: {str(e)}"
        )  
        
        
@router.put("/actualizar/{ayuda_id}", response_model=AyudaResponse, status_code=status.HTTP_200_OK)
async def update_ayuda_endpoint(
    ayuda_id: int, ayuda: AyudaCreate, db: AsyncSession = Depends(get_db_anserma)
):
    """
    Actualiza una ayuda existente.
    
    :param ayuda_id: ID de la ayuda a actualizar
    :param ayuda: Datos nuevos de la ayuda
    :param db: Sesión de base de datos
    :return: Ayuda actualizada o un error HTTP
    """
    try:
        updated_ayuda = await update_ayuda(db, ayuda_id, ayuda)
        if not updated_ayuda:
            raise HTTPException(status_code=404, detail="Ayuda no encontrada")
        return updated_ayuda
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar ayuda: {str(e)}"
        )


@router.delete("/eliminar/{ayuda_id}", status_code=status.HTTP_204_NO_CONTENT)
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
