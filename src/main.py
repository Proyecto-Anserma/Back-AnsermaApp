from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from src.controladores.ciudadano_controlador import ciudadanos_controlador
from src.controladores.usuario_controlador import usuarios_controlador

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Permite solicitudes de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.title = "Back-AnsermaApp"

# Inclusión de routers
app.include_router(router=ciudadanos_controlador)
app.include_router(router=usuarios_controlador)
