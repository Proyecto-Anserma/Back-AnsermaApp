from fastapi import APIRouter
from src.modulos.ciudadano.ciudadano_rutas import router as ciudadano_router
from src.modulos.solicitud.solicitud_rutas import router as solicitud_router
from src.modulos.referencias.referencias_rutas import router as referencias_router
from src.modulos.ubicacion.ubicacion_rutas import router as ubicacion_router

router = APIRouter()

# Incluir routers de cada módulo
router.include_router(ciudadano_router, prefix="/ciudadanos", tags=["ciudadanos"])
router.include_router(solicitud_router, prefix="/solicitudes", tags=["solicitudes"])
router.include_router(referencias_router, prefix="/referencias", tags=["referencias"])
router.include_router(ubicacion_router, prefix="/ubicaciones", tags=["ubicaciones"])

def include_routes(app):
    app.include_router(router)
