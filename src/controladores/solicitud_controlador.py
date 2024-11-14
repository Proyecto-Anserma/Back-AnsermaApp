from fastapi import Body, APIRouter
from ..modulos.ciudadano.ciudadano_db_modelo import Ciudadano
from ..modulos.ciudadano.consultar_ciudadanos import consultar_ciudadanos

ciudadanos_controlador = APIRouter()


@ciudadanos_controlador.post(
    '/consultar-ciudadanos',
    tags=['Ciudadanos'],
    response_model=list[Ciudadano]  #RESPONDE AL FRONT
)
async def consultar_ciudadanos_endpoint(
    cedula: str = Body(..., embed=True)  #PIDE DEL FRONT
):
    return consultar_ciudadanos(cedula)



