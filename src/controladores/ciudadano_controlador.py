from fastapi import Body, APIRouter
from src.Servicios.ciudadano_servicio import consultar_ciudadanos

ciudadanos_controlador = APIRouter()

@ciudadanos_controlador.post('/consultar-ciudadanos', tags=['Ciudadanos'])
def consultar_ciudadanos_endpoint(id: int = Body(), title: str = Body()):
    ciudadanos = []  # Define ciudadanos como una lista vacía
    ciudadano = consultar_ciudadanos(id, title)  
    ciudadanos.append(ciudadano)
    return ciudadanos  # O devuelve ciudadanos si necesitas todos los datos acumulados
