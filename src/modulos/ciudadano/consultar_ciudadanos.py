from .ciudadano_db_modelo import Ciudadano
from datetime import date

def consultar_ciudadanos(cedula: str):
    ciudadanos = [
        Ciudadano(
            nombre_ciudadano="Miguel",
            apellido_ciudadano="Ramos",
            fecha_nacimiento_ciudadano=date(1990, 5, 15),  
            correo_electronico_ciudadano="miguel@gmail.com",  
            telefono_ciudadano="123123",
            geolocalizacion="asdsd"
        ),
        Ciudadano(
            nombre_ciudadano="Miguel",
            apellido_ciudadano="Ramos",
            fecha_nacimiento_ciudadano=date(1990, 5, 15),  
            correo_electronico_ciudadano="miguel@gmail.com",  
            telefono_ciudadano="123123",
            geolocalizacion="asdsd"
        ),  
    ]
    return ciudadanos
