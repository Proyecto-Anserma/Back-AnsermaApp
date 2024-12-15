from fastapi import APIRouter
from src.modulos.ciudadano.ciudadano_rutas import router as ciudadano_router
from src.modulos.solicitud.solicitud_rutas import router as solicitud_router
from src.modulos.solicitud_ayuda.solicitud_ayuda_rutas import router as solicitud_ayuda_router
from src.modulos.ayuda.ayuda_rutas import router as ayuda_router
from src.modulos.cantidad_origen_ayuda.cantidad_origen_ayuda_rutas import router as cantidad_origen_ayuda_router
from src.modulos.referencias.referencias_rutas import router as referencias_router
from src.modulos.ubicacion.ubicacion_rutas import router as ubicacion_router
from src.modulos.estado_solicitud.estado_solicitud_rutas import router as estado_solicitud_router
from src.modulos_usuarios.usuario.usuario_rutas import router as usuario_router
from src.modulos.tipo_solicitud.tipo_solicitud_rutas import router as tipo_solicitud_router
from src.modulos.pertenencia_etnica.pertenencia_etnica_rutas import router as pertenencia_etnica_router

from src.modulos.genero.genero_rutas import router as genero_router
from src.auth import auth_rutas
from src.modulos.estado.estado_rutas import router as estado_router
from src.modulos.origen_ayuda.origen_ayuda_rutas import router as origen_ayuda_router





router = APIRouter()

# Incluir routers de cada módulo
router.include_router(ciudadano_router, prefix="/ciudadanos", tags=["ciudadanos"])
router.include_router(solicitud_router, prefix="/solicitudes", tags=["solicitudes"])
router.include_router(estado_solicitud_router, prefix="/estado_solicitudes", tags=["estado_solicitudes"])
router.include_router(solicitud_ayuda_router, prefix="/solicitudes_ayuda", tags=["solicitudes_ayudas"])
router.include_router(ayuda_router, prefix="/ayudas", tags=["ayudas"])
router.include_router(origen_ayuda_router, prefix="/origenes_ayuda", tags=["origenes_ayudas"])
router.include_router(cantidad_origen_ayuda_router, prefix="/cantidades_origen_ayuda", tags=["cantidades_origenes_ayudas"])
router.include_router(ubicacion_router, prefix="/ubicaciones", tags=["ubicaciones"])
router.include_router(usuario_router, prefix="/usuarios", tags=["usuarios"])
router.include_router(referencias_router, prefix="/referencias", tags=["referencias"])

router.include_router(tipo_solicitud_router, prefix="/tipo_solicitud", tags=["tipo_solicitud"])
router.include_router(pertenencia_etnica_router, prefix="/pertenencia_etnica", tags=["pertenencia_etnica"])

router.include_router(genero_router, prefix="/genero", tags=["genero"])

router.include_router(auth_rutas.router, tags=["authentication"])

router.include_router(estado_router, prefix="/api", tags=["Estados"])
router.include_router(origen_ayuda_router, prefix="/api", tags=["Origenes de ayuda"])

def include_routes(app):
    app.include_router(router)
