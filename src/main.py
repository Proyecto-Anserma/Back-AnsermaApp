from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db_config import database_anserma, database_usuarios, BaseAnserma, BaseUsuarios, engine_anserma, engine_usuarios
from src import rutas

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a las bases de datos
@app.on_event("startup")
async def startup():
    await database_anserma.connect()
    await database_usuarios.connect()

@app.on_event("shutdown")
async def shutdown():
    await database_anserma.disconnect()
    await database_usuarios.disconnect()

# Incluye las rutas definidas en el módulo rutas
rutas.include_routes(app)

