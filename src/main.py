from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse
from src.controladores.ciudadano_controlador import ciudadanos_controlador
from src.controladores.usuario_controlador import usuarios_controlador


app = FastAPI()
app.title = "Back-AnsermaApp"




app.include_router(router=ciudadanos_controlador)
app.include_router(router=usuarios_controlador)





