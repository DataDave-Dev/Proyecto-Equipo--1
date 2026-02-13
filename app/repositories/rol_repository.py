# Repositorio de roles - queries contra la tabla Roles

from app.database.connection import get_connection
from app.models.Rol import Rol


class RolRepository:

    def find_all(self):
        # obtener todos los roles disponibles en el sistema
        conn = get_connection()
        cursor = conn.execute(
            "SELECT * FROM Roles ORDER BY NombreRol",
        )
        rows = cursor.fetchall()
        # convertir cada fila en un objeto Rol
        return [self._row_to_rol(row) for row in rows]

    def find_by_id(self, rol_id):
        # buscar un rol específico por su ID
        conn = get_connection()
        cursor = conn.execute(
            "SELECT * FROM Roles WHERE RolID = ?",
            (rol_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_rol(row)

    @staticmethod
    def _row_to_rol(row):
        # convertir el Row de sqlite a nuestro modelo Rol
        return Rol(
            rol_id=row["RolID"],
            nombre_rol=row["NombreRol"],
            descripcion=row["Descripcion"],
            fecha_creacion=row["FechaCreacion"],
        )
