# Configuracion centralizada de todos los catalogos del sistema
# Cada catalogo define su tabla, columnas, validaciones y relaciones

CATALOGO_CONFIGS = {
    # --- Ventas ---
    'etapas_venta': {
        'table': 'EtapasVenta',
        'id_column': 'EtapaID',
        'display_name': 'Etapas de Venta',
        'display_name_singular': 'Etapa de Venta',
        'category': 'Ventas',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'Orden', 'label': 'Orden', 'required': True, 'type': 'int'},
            {'name': 'Probabilidad', 'label': 'Probabilidad (%)', 'required': False, 'type': 'float'},
            {'name': 'Color', 'label': 'Color', 'required': False, 'type': 'color'},
            {'name': 'Descripcion', 'label': 'Descripcion', 'required': False, 'type': 'text'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Orden',
        'referenced_by': [
            {'table': 'Oportunidades', 'column': 'EtapaID'},
        ],
    },
    'motivos_perdida': {
        'table': 'MotivosPerdida',
        'id_column': 'MotivoID',
        'display_name': 'Motivos de Perdida',
        'display_name_singular': 'Motivo de Perdida',
        'category': 'Ventas',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'Descripcion', 'label': 'Descripcion', 'required': False, 'type': 'text'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Oportunidades', 'column': 'MotivosPerdidaID'},
        ],
    },

    # --- Actividades ---
    'tipos_actividad': {
        'table': 'TiposActividad',
        'id_column': 'TipoActividadID',
        'display_name': 'Tipos de Actividad',
        'display_name_singular': 'Tipo de Actividad',
        'category': 'Actividades',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'Icono', 'label': 'Icono', 'required': False, 'type': 'text'},
            {'name': 'Color', 'label': 'Color', 'required': False, 'type': 'color'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Actividades', 'column': 'TipoActividadID'},
        ],
    },
    'prioridades': {
        'table': 'Prioridades',
        'id_column': 'PrioridadID',
        'display_name': 'Prioridades',
        'display_name_singular': 'Prioridad',
        'category': 'Actividades',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'Nivel', 'label': 'Nivel', 'required': True, 'type': 'int'},
            {'name': 'Color', 'label': 'Color', 'required': False, 'type': 'color'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Nivel',
        'referenced_by': [
            {'table': 'Actividades', 'column': 'PrioridadID'},
        ],
    },
    'estados_actividad': {
        'table': 'EstadosActividad',
        'id_column': 'EstadoActividadID',
        'display_name': 'Estados de Actividad',
        'display_name_singular': 'Estado de Actividad',
        'category': 'Actividades',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Actividades', 'column': 'EstadoActividadID'},
        ],
    },

    # --- Contactos ---
    'industrias': {
        'table': 'Industrias',
        'id_column': 'IndustriaID',
        'display_name': 'Industrias',
        'display_name_singular': 'Industria',
        'category': 'Contactos',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'Descripcion', 'label': 'Descripcion', 'required': False, 'type': 'text'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Empresas', 'column': 'IndustriaID'},
        ],
    },
    'tamanos_empresa': {
        'table': 'TamanosEmpresa',
        'id_column': 'TamanoID',
        'display_name': 'Tamanos de Empresa',
        'display_name_singular': 'Tamano de Empresa',
        'category': 'Contactos',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'RangoEmpleados', 'label': 'Rango de Empleados', 'required': False, 'type': 'text'},
            {'name': 'Descripcion', 'label': 'Descripcion', 'required': False, 'type': 'text'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Empresas', 'column': 'TamanoID'},
        ],
    },
    'origenes_contacto': {
        'table': 'OrigenesContacto',
        'id_column': 'OrigenID',
        'display_name': 'Origenes de Contacto',
        'display_name_singular': 'Origen de Contacto',
        'category': 'Contactos',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'Descripcion', 'label': 'Descripcion', 'required': False, 'type': 'text'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Contactos', 'column': 'OrigenID'},
            {'table': 'Empresas', 'column': 'OrigenID'},
            {'table': 'Oportunidades', 'column': 'OrigenID'},
        ],
    },

    # --- Finanzas ---
    'monedas': {
        'table': 'Monedas',
        'id_column': 'MonedaID',
        'display_name': 'Monedas',
        'display_name_singular': 'Moneda',
        'category': 'Finanzas',
        'columns': [
            {'name': 'Codigo', 'label': 'Codigo', 'required': True, 'type': 'text'},
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'Simbolo', 'label': 'Simbolo', 'required': False, 'type': 'text'},
        ],
        'unique_column': 'Codigo',
        'order_by': 'Codigo',
        'referenced_by': [
            {'table': 'Empresas', 'column': 'MonedaID'},
            {'table': 'Oportunidades', 'column': 'MonedaID'},
            {'table': 'Productos', 'column': 'MonedaID'},
        ],
    },
}

# Configuracion separada para catalogos geograficos (cascada)
GEOGRAFIA_CONFIGS = {
    'paises': {
        'table': 'Paises',
        'id_column': 'PaisID',
        'display_name': 'Paises',
        'display_name_singular': 'Pais',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
            {'name': 'CodigoISO', 'label': 'Codigo ISO', 'required': False, 'type': 'text'},
        ],
        'unique_column': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Estados', 'column': 'PaisID'},
        ],
    },
    'estados': {
        'table': 'Estados',
        'id_column': 'EstadoID',
        'display_name': 'Estados',
        'display_name_singular': 'Estado',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
        ],
        'fk_column': 'PaisID',
        'fk_parent_table': 'Paises',
        'fk_parent_id': 'PaisID',
        'fk_parent_display': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Ciudades', 'column': 'EstadoID'},
        ],
    },
    'ciudades': {
        'table': 'Ciudades',
        'id_column': 'CiudadID',
        'display_name': 'Ciudades',
        'display_name_singular': 'Ciudad',
        'columns': [
            {'name': 'Nombre', 'label': 'Nombre', 'required': True, 'type': 'text'},
        ],
        'fk_column': 'EstadoID',
        'fk_parent_table': 'Estados',
        'fk_parent_id': 'EstadoID',
        'fk_parent_display': 'Nombre',
        'order_by': 'Nombre',
        'referenced_by': [
            {'table': 'Contactos', 'column': 'CiudadID'},
            {'table': 'Empresas', 'column': 'CiudadID'},
        ],
    },
}

# Orden de categorias para el sub-sidebar
CATEGORIAS_ORDEN = [
    'Ventas',
    'Actividades',
    'Contactos',
    'Finanzas',
    'Geografia',
]
