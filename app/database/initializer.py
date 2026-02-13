# Se encarga de crear las tablas y meter datos iniciales la primera vez

import os
import bcrypt
from app.config.settings import DB_PATH, SCHEMA_PATH
from app.database.connection import get_connection


def initialize_database():
    # si la base de datos ya existe, no inicializar
    if os.path.exists(DB_PATH):
        return

    conn = get_connection()
    # leer y ejecutar el .sql con la estructura de tablas
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    _seed_default_data(conn)


def _seed_default_data(conn):
    # Si no existe ningun usuario en la tabla de Usuarios crea el administrador por defecto
    cursor = conn.execute("SELECT COUNT(*) FROM Usuarios")
    if cursor.fetchone()[0] == 0:
        hashed = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn.execute(
            "INSERT INTO Usuarios (Nombre, ApellidoPaterno, Email, ContrasenaHash, RolID) "
            "VALUES (?, ?, ?, ?, ?)",
            ("Admin", "Sistema", "admin@crm.com", hashed, 1),
        )
        conn.commit()
