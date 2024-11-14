from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .ciudadano_servicio import get_ciudadanos
from database.db import get_db

router = APIRouter()

@router.get("/ciudadanos/")
async def read_ciudadanos(db: AsyncSession = Depends(get_db)):
    return await get_ciudadanos(db)


'''@router.post(
    '/consultar-ciudadanos',
    tags=['Ciudadanos'],
    response_model=list[Ciudadano]  #RESPONDE AL FRONT
)
async def consultar_ciudadanos_endpoint(
    cedula: str = Body(..., embed=True)  #PIDE DEL FRONT
):
    return consultar_ciudadanos(cedula)'''