from fastapi import Body, APIRouter


usuarios_controlador = APIRouter()



@usuarios_controlador.post('/consultar-usuarios', tags=['Usuarios'])
def consultar_usuarios(id: int = Body(), title: str = Body()):
    usuarios.append({
        'id': id,
        'title': title
    })