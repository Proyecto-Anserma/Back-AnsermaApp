from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .solicitud_ayuda_modelos import SolicitudAyudaCreate, SolicitudAyudaResponse
from database.db_config import get_db_anserma
from .solicitud_ayuda_servicio import get_solicitudes_ayuda, create_solicitud_ayuda, update_solicitud_ayuda, delete_solicitud_ayuda
from src.auth.auth_utils import get_current_user
from src.modulos_usuarios.usuario.usuario_db_modelo import Usuario
from .solicitud_ayuda_db_modelo import SolicitudAyuda

router = APIRouter()

@router.get("/solicitudes-ayuda/", response_model=List[SolicitudAyudaResponse])
async def read_solicitudes_ayuda(db: AsyncSession = Depends(get_db_anserma)):
    try:
        solicitudes_ayuda = await get_solicitudes_ayuda(db)
        return solicitudes_ayuda
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener solicitudes de ayuda: {str(e)}"
        )

@router.post("/solicitudes-ayuda/", response_model=SolicitudAyudaResponse, status_code=status.HTTP_201_CREATED)
async def create_solicitud_ayuda_endpoint(
    solicitud_ayuda: SolicitudAyudaCreate, 
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        result = await create_solicitud_ayuda(db, solicitud_ayuda)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la solicitud de ayuda: {str(e)}"
        )
        

@router.put(
    "/solicitudes-ayuda/{solicitud_ayuda_id}",
    response_model=SolicitudAyudaResponse,
    status_code=status.HTTP_200_OK
)
async def update_solicitud_ayuda_endpoint(
    solicitud_ayuda_id: int,
    solicitud_ayuda: SolicitudAyudaCreate,
    db: AsyncSession = Depends(get_db_anserma)
):
    """
    Actualiza una solicitud de ayuda existente.

    :param solicitud_ayuda_id: ID de la solicitud de ayuda a actualizar
    :param solicitud_ayuda: Datos nuevos para actualizar
    :param db: Sesión de base de datos
    :return: La solicitud de ayuda actualizada o un error HTTP
    """
    try:
        updated_solicitud = await update_solicitud_ayuda(db, solicitud_ayuda_id, solicitud_ayuda)
        if not updated_solicitud:
            raise HTTPException(
                status_code=404,
                detail="Solicitud de ayuda no encontrada"
            )
        return updated_solicitud
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar solicitud de ayuda: {str(e)}"
        )


@router.delete("/solicitudes-ayuda/{solicitud_ayuda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solicitud_ayuda_endpoint(
    solicitud_ayuda_id: int, 
    db: AsyncSession = Depends(get_db_anserma)
):
    try:
        deleted = await delete_solicitud_ayuda(db, solicitud_ayuda_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Solicitud de ayuda no encontrada")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar solicitud de ayuda: {str(e)}"
        )

async def create_solicitud(db: AsyncSession, solicitud_data: dict):
    try:
        print(f"Datos recibidos: {solicitud_data}")  # Debug
        nueva_solicitud = SolicitudAyuda(**solicitud_data)
        db.add(nueva_solicitud)
        await db.commit()
        await db.refresh(nueva_solicitud)
        return nueva_solicitud
    except Exception as e:
        print(f"Error creando solicitud: {str(e)}")  # Debug
        await db.rollback()
        raise