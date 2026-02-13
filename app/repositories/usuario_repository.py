# Repositorio de usuarios - queries contra la tabla Usuarios

from app.database.connection import get_connection
from app.models.Usuario import Usuario


class UsuarioRepository:

    def find_by_email(self, email):
        # buscar usuario activo por email
        conn = get_connection()
        cursor = conn.execute(
            "SELECT * FROM Usuarios WHERE Email = ? AND Activo = 1",
            (email,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_usuario(row)

    def update_ultimo_acceso(self, usuario_id, timestamp):
        conn = get_connection()
        conn.execute(
            "UPDATE Usuarios SET UltimoAcceso = ? WHERE UsuarioID = ?",
            (timestamp, usuario_id),
        )
        conn.commit()

    def find_all(self):
        # obtener todos los usuarios del sistema con información de su rol
        conn = get_connection()
        cursor = conn.execute(
            """
            SELECT u.*, r.NombreRol
            FROM Usuarios u
            LEFT JOIN Roles r ON u.RolID = r.RolID
            ORDER BY u.FechaCreacion DESC
            """
        )
        rows = cursor.fetchall()
        # convertir cada fila a un objeto Usuario (incluye nombre_rol automáticamente)
        return [self._row_to_usuario(row) for row in rows]

    def email_exists(self, email, excluir_id=None):
        # verificar si ya existe un usuario con este email
        conn = get_connection()
        if excluir_id:
            cursor = conn.execute(
                "SELECT COUNT(*) as total FROM Usuarios WHERE Email = ? AND UsuarioID != ?",
                (email, excluir_id),
            )
        else:
            cursor = conn.execute(
                "SELECT COUNT(*) as total FROM Usuarios WHERE Email = ?",
                (email,),
            )
        result = cursor.fetchone()
        return result["total"] > 0

    def create(self, usuario):
        # insertar un nuevo usuario en la base de datos
        conn = get_connection()
        cursor = conn.execute(
            """
            INSERT INTO Usuarios (
                Nombre, ApellidoPaterno, ApellidoMaterno, Email,
                Telefono, ContrasenaHash, RolID, Activo, FotoPerfil
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                usuario.nombre,
                usuario.apellido_paterno,
                usuario.apellido_materno,
                usuario.email,
                usuario.telefono,
                usuario.contrasena_hash,
                usuario.rol_id,
                usuario.activo,
                usuario.foto_perfil,
            ),
        )
        conn.commit()
        # retornar el id del usuario recién creado
        return cursor.lastrowid

    def update(self, usuario):
        # actualizar un usuario existente en la base de datos
        conn = get_connection()
        conn.execute(
            """
            UPDATE Usuarios SET
                Nombre = ?, ApellidoPaterno = ?, ApellidoMaterno = ?,
                Email = ?, Telefono = ?, RolID = ?, Activo = ?
            WHERE UsuarioID = ?
            """,
            (
                usuario.nombre,
                usuario.apellido_paterno,
                usuario.apellido_materno,
                usuario.email,
                usuario.telefono,
                usuario.rol_id,
                usuario.activo,
                usuario.usuario_id,
            ),
        )
        conn.commit()

    def update_password(self, usuario_id, contrasena_hash):
        # actualizar solo la contraseña de un usuario
        conn = get_connection()
        conn.execute(
            "UPDATE Usuarios SET ContrasenaHash = ? WHERE UsuarioID = ?",
            (contrasena_hash, usuario_id),
        )
        conn.commit()

    @staticmethod
    def _row_to_usuario(row):
        # convertir el Row de sqlite a nuestro modelo Usuario
        # intentar obtener el nombre del rol si está disponible en la consulta
        nombre_rol = None
        try:
            nombre_rol = row["NombreRol"] if row["NombreRol"] else "Sin rol"
        except (KeyError, IndexError):
            # el campo NombreRol no está en el resultado de la consulta
            nombre_rol = None

        return Usuario(
            usuario_id=row["UsuarioID"],
            nombre=row["Nombre"],
            apellido_paterno=row["ApellidoPaterno"],
            apellido_materno=row["ApellidoMaterno"],
            email=row["Email"],
            telefono=row["Telefono"],
            contrasena_hash=row["ContrasenaHash"],
            rol_id=row["RolID"],
            activo=row["Activo"],
            foto_perfil=row["FotoPerfil"],
            fecha_creacion=row["FechaCreacion"],
            ultimo_acceso=row["UltimoAcceso"],
            nombre_rol=nombre_rol,
        )
