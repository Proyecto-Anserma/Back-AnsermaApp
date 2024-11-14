from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import database, Base, engine  # Importamos database, Base y engine
from src import rutas 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

rutas.include_routes(app)
