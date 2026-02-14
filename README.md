# CRM - Sistema de Gestion de Relaciones con Clientes

Aplicacion de escritorio para la gestion de relaciones con clientes (CRM), desarrollada como proyecto academico para la materia de **Base de Datos y Lenguajes** en la Facultad de Ingeniería Mecanica y Eléctrica (FIME) de la Universidad Autonoma de Nuevo Leon (UANL).

---

## Lenguaje y tecnologias

| Tecnologia | Version | Proposito |
|---|---|---|
| Python | 3.x | Lenguaje principal |
| PyQt5 | 5.15.11 | Framework de interfaz grafica |
| SQLite3 | (incluido en Python) | Motor de base de datos |
| bcrypt | 5.0.0 | Hashing seguro de contraseñas |

---

## Paradigmas y patrones de diseno

- **MVC (Modelo-Vista-Controlador)**: separacion clara entre la logica de negocio, la presentacion y el control del flujo.
- **Patron Repository**: capa de acceso a datos desacoplada de la logica de negocio.
- **Arquitectura por capas**: cada capa tiene una responsabilidad unica.
- **Singleton**: conexion a base de datos reutilizable a nivel global.
- **Generacion dinamica de UI**: los formularios de catalogos se construyen en tiempo de ejecucion a partir de configuracion centralizada.
- **Signal-Slot (PyQt5)**: comunicacion desacoplada entre componentes de la interfaz.

### Flujo de capas

```
Views (Presentacion)
    |
Controllers (Control de flujo)
    |
Services (Logica de negocio)
    |
Repositories (Acceso a datos)
    |
Database (SQLite)
```

---

## Estructura de carpetas

```
Proyecto Equipo #1/
├── app/                            # Paquete principal de la aplicacion
│   ├── assets/                     # Iconos SVG para la interfaz
│   ├── config/                     # Configuracion de la app y catalogos
│   │   ├── settings.py
│   │   └── catalogos.py
│   ├── database/                   # Capa de base de datos
│   │   ├── connection.py           # Conexion singleton a SQLite
│   │   └── initializer.py         # Creacion de esquema y datos iniciales
│   ├── models/                     # Modelos de datos
│   │   ├── Usuario.py
│   │   ├── Rol.py
│   │   └── Catalogo.py
│   ├── repositories/               # Capa de acceso a datos (CRUD)
│   │   ├── usuario_repository.py
│   │   ├── rol_repository.py
│   │   └── catalogo_repository.py
│   ├── services/                   # Capa de logica de negocio
│   │   ├── auth_service.py
│   │   ├── usuario_service.py
│   │   └── catalogo_service.py
│   ├── controllers/                # Controladores MVC
│   │   ├── login_controller.py
│   │   └── main_controller.py
│   └── views/                      # Vistas e interfaz grafica
│       ├── ui/                     # Archivos .ui (Qt Designer)
│       ├── login_view.py
│       ├── main_view.py
│       ├── configuracion_view.py
│       ├── catalogo_list_widget.py
│       ├── catalogo_form_dialog.py
│       └── geografia_widget.py
├── db/                             # Base de datos y esquema SQL
│   ├── database_query.sql          # Esquema completo (60+ tablas)
│   └── crm.db                     # Archivo SQLite generado
├── tests/                          # Pruebas (pendiente)
├── Docs/                           # Documentacion del proyecto
├── main.py                         # Punto de entrada de la aplicacion
├── requirements.txt                # Dependencias de Python
└── README.md
```

---

## Base de datos

El esquema SQLite contiene **mas de 60 tablas**, 7 vistas, triggers e indices. A continuacion los modulos principales:

| Modulo | Tablas principales | Descripcion |
|---|---|---|
| Usuarios | `Usuarios`, `Roles` | Autenticacion y control de acceso |
| Contactos | `Empresas`, `Contactos` | Gestion de cuentas y personas |
| Ventas | `Oportunidades`, `Cotizaciones`, `Productos` | Pipeline comercial |
| Actividades | `Actividades`, `TiposActividad` | Llamadas, reuniones, tareas |
| Campañas | `Campanas`, `Segmentos`, `Etiquetas` | Marketing y segmentacion |
| Geografia | `Paises`, `Estados`, `Ciudades` | Jerarquia geografica |
| Catalogos | `Industrias`, `Monedas`, `Prioridades`, etc. | Tablas de configuracion |
| Auditoria | `LogAuditoria`, `Notificaciones` | Trazabilidad y alertas |

### Caracteristicas de la BD

- Claves foraneas con integridad referencial
- Triggers para timestamps automaticos, historial de etapas y auditoria
- Vistas precalculadas para reportes (pipeline, rendimiento, conversion)
- Modo WAL para mejor rendimiento concurrente

---

## Instalacion y ejecucion

```bash
# Clonar el repositorio
git clone <url-del-repositorio>

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicacion
python main.py
```

La base de datos se crea automaticamente en la primera ejecucion con datos iniciales precargados (roles, catalogos, datos geograficos y un usuario administrador).

### Credenciales por defecto

| Campo | Valor |
|---|---|
| Email | `admin@crm.com` |
| Contrasena | `admin123` |

---

## Modulos implementados

- [x] Autenticacion (login con bcrypt)
- [x] Gestion de usuarios (CRUD completo)
- [x] Gestion de catalogos generica (13 tipos de catalogo)
- [x] Jerarquia geografica (Paises, Estados, Ciudades)
- [x] Configuracion con navegacion por pestañas
- [ ] Gestion de contactos y empresas
- [ ] Pipeline de oportunidades
- [ ] Gestion de actividades
- [ ] Campañas de marketing
- [ ] Reportes y dashboards
- [ ] Gestion de documentos
- [ ] Recordatorios y notificaciones

---

## Validaciones

- Correo electronico con formato valido (regex)
- Telefono de 10 digitos
- Contraseña minimo 8 caracteres
- Campos requeridos y restricciones de unicidad
- Proteccion contra eliminacion de registros referenciados

---

## Equipo

Proyecto academico - **Equipo #1**
Materia: Base de Datos y Lenguajes | FIME | UANL
Catedrático: M.C. Jorge Alejandro Lozano Gonzalez
