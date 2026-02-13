# Modelo de Rol - representa un registro de la tabla Roles

from datetime import datetime


class Rol:
    def __init__(
        self,
        rol_id=None,
        nombre_rol="",
        descripcion=None,
        fecha_creacion=None
    ):
        self.rol_id = rol_id
        self.nombre_rol = nombre_rol
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"<Rol(id={self.rol_id}, nombre='{self.nombre_rol}')>"
