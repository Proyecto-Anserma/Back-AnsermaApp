from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.elements import WKTElement
from typing import List
from shapely import wkt
from .ciudadano_db_modelo import Ciudadano
from .ciudadano_modelos import CiudadanoCreate, CiudadanoResponse, CiudadanoUpdate
from database.db import get_db
from .ciudadano_servicio import (
    get_ciudadanos,
    create_ciudadano,
    update_ciudadano,
    delete_ciudadano,
)

router = APIRouter()

@router.get("/ciudadanos/", response_model=List[CiudadanoResponse])
async def read_ciudadanos(db: AsyncSession = Depends(get_db)):
    try:
        ciudadanos = await get_ciudadanos(db)
        return ciudadanos
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener ciudadanos: {str(e)}"
        )


@router.post("/ciudadanos/", response_model=CiudadanoResponse, status_code=status.HTTP_201_CREATED)
async def create_ciudadano_endpoint(ciudadano: CiudadanoCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Procesamos el campo de geometría
        geom_str = ciudadano.geolocalizacion
        if geom_str.startswith('SRID='):
            srid = int(geom_str.split(';')[0].replace('SRID=', ''))
            wkt_str = geom_str.split(';')[1]
        else:
            srid = 4326
            wkt_str = geom_str
        
        # Preparamos los datos
        ciudadano_dict = ciudadano.model_dump()
        ciudadano_dict['geolocalizacion'] = WKTElement(wkt_str, srid=srid)
        
        # Convertimos el teléfono a integer si es necesario
        ciudadano_dict['telefono_ciudadano'] = int(ciudadano_dict['telefono_ciudadano'])
        
        # Creamos el ciudadano
        nuevo_ciudadano = Ciudadano(**ciudadano_dict)
        db.add(nuevo_ciudadano)
        await db.commit()
        await db.refresh(nuevo_ciudadano)
        
        return nuevo_ciudadano
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear ciudadano: {str(e)}"
        )
        
@router.put("/ciudadanos/{ciudadano_id}", response_model=CiudadanoResponse)
async def update_ciudadano_endpoint(
    ciudadano_id: str, 
    ciudadano: CiudadanoUpdate, 
    db: AsyncSession = Depends(get_db)
):
    try:
        updated_ciudadano = await update_ciudadano(db, ciudadano_id, ciudadano)
        if not updated_ciudadano:
            raise HTTPException(status_code=404, detail="Ciudadano no encontrado")
        return updated_ciudadano
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al actualizar ciudadano: {str(e)}"
        )

@router.delete("/ciudadanos/{ciudadano_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ciudadano_endpoint(ciudadano_id: str, db: AsyncSession = Depends(get_db)):
    try:
        deleted = await delete_ciudadano(db, ciudadano_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Ciudadano no encontrado")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar ciudadano: {str(e)}"
        )