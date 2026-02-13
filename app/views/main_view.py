# Vista principal del CRM - carga el .ui y muestra datos del usuario

import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QCheckBox, QMessageBox,
    QScrollArea, QFrame, QGridLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PyQt5.QtGui import QIcon, QCursor, QColor
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic
from app.services.usuario_service import UsuarioService
from app.repositories.rol_repository import RolRepository

UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "main_view.ui")
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets")


class MainView(QMainWindow):

    def __init__(self, usuario):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self._usuario_actual = usuario
        self._usuario_service = UsuarioService()
        self._rol_repository = RolRepository()
        self._usuario_editando = None  # None = modo crear, Usuario = modo editar
        self._setup_icons()
        self._set_user_data(usuario)
        self._setup_navigation()
        self._create_lista_usuarios()
        self._create_form_usuarios()

    def _setup_icons(self):
        logout_icon = QIcon(os.path.join(ASSETS_PATH, "logout.svg"))
        self.btnCerrarSesion.setIcon(logout_icon)
        self.btnCerrarSesion.setIconSize(QSize(20, 20))

    def _set_user_data(self, usuario):
        nombre_completo = f"{usuario.nombre} {usuario.apellido_paterno}"
        self.headerUserName.setText(nombre_completo)
        self.welcomeTitle.setText(f"Bienvenido, {usuario.nombre}")

    def _setup_navigation(self):
        # conectar los botones de navegación del sidebar
        self.sidebar_buttons = []

        # lista de todos los botones de navegación para poder cambiar estilos
        if hasattr(self, 'btnDashboard'):
            self.sidebar_buttons.append(self.btnDashboard)
        if hasattr(self, 'btnClientes'):
            self.sidebar_buttons.append(self.btnClientes)
        if hasattr(self, 'btnProductos'):
            self.sidebar_buttons.append(self.btnProductos)
        if hasattr(self, 'btnVentas'):
            self.sidebar_buttons.append(self.btnVentas)
        if hasattr(self, 'btnReportes'):
            self.sidebar_buttons.append(self.btnReportes)
        if hasattr(self, 'btnUsuarios'):
            self.sidebar_buttons.append(self.btnUsuarios)
            # conectar el botón de Usuarios para mostrar la lista
            self.btnUsuarios.clicked.connect(self._mostrar_seccion_usuarios)
        if hasattr(self, 'btnConfiguracion'):
            self.sidebar_buttons.append(self.btnConfiguracion)

    def _resaltar_boton_activo(self, boton_activo):
        # resetear el estilo de todos los botones del sidebar
        estilo_normal = """
            background-color: transparent;
            color: #a0aec0;
            font-size: 15px;
            font-weight: 500;
            text-align: left;
            padding: 14px 20px;
            border: none;
            border-radius: 8px;
            margin: 2px 12px;
        """

        estilo_activo = """
            background-color: #4a90d9;
            color: #ffffff;
            font-size: 15px;
            font-weight: 600;
            text-align: left;
            padding: 14px 20px;
            border: none;
            border-radius: 8px;
            margin: 2px 12px;
        """

        # aplicar estilo normal a todos los botones
        for boton in self.sidebar_buttons:
            boton.setStyleSheet(estilo_normal)

        # aplicar estilo activo al botón seleccionado
        if boton_activo:
            boton_activo.setStyleSheet(estilo_activo)

    def _create_lista_usuarios(self):
        # crear el widget de lista de usuarios con diseño mejorado
        self.lista_usuarios_widget = QWidget()
        lista_layout = QVBoxLayout(self.lista_usuarios_widget)
        lista_layout.setContentsMargins(0, 0, 0, 0)
        lista_layout.setSpacing(25)

        # cabecera con título y botón nuevo
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # contenedor del título y subtítulo
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        titulo = QLabel("Gestión de Usuarios")
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #1a1a2e;")
        title_layout.addWidget(titulo)

        subtitulo = QLabel("Administra y visualiza todos los usuarios del sistema")
        subtitulo.setStyleSheet("font-size: 15px; color: #7f8c9b;")
        title_layout.addWidget(subtitulo)

        header_layout.addWidget(title_container)
        header_layout.addStretch()

        # botón para crear nuevo usuario
        self.btn_nuevo_usuario = QPushButton("+ Nuevo Usuario")
        self.btn_nuevo_usuario.setFixedSize(180, 50)
        self.btn_nuevo_usuario.setStyleSheet("""
            QPushButton {
                background-color: #4a90d9;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #3a7bc8;
            }
            QPushButton:pressed {
                background-color: #2a6bb8;
            }
        """)
        self.btn_nuevo_usuario.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_nuevo_usuario.clicked.connect(self._mostrar_form_nuevo_usuario)
        header_layout.addWidget(self.btn_nuevo_usuario)

        lista_layout.addWidget(header_container)

        # tarjetas de estadísticas rápidas
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(20)

        # tarjeta total de usuarios
        self.card_total_usuarios = self._create_stat_card("Total Usuarios", "0", "#4a90d9")
        stats_layout.addWidget(self.card_total_usuarios, 1)

        # tarjeta usuarios activos
        self.card_usuarios_activos = self._create_stat_card("Usuarios Activos", "0", "#48bb78")
        stats_layout.addWidget(self.card_usuarios_activos, 1)

        # tarjeta usuarios inactivos
        self.card_usuarios_inactivos = self._create_stat_card("Usuarios Inactivos", "0", "#f56565")
        stats_layout.addWidget(self.card_usuarios_inactivos, 1)

        lista_layout.addWidget(stats_container)

        # crear tabla de usuarios con mejor diseño
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(7)
        self.tabla_usuarios.setHorizontalHeaderLabels([
            "ID", "Nombre Completo", "Email", "Teléfono", "Rol", "Estado", "Fecha Registro"
        ])

        # configurar apariencia de la tabla mejorada
        self.tabla_usuarios.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                gridline-color: #f0f2f5;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f7fafc;
                color: #2d3748;
                font-weight: bold;
                font-size: 14px;
                padding: 15px 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                border-right: 1px solid #f0f2f5;
            }
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;
                border-right: none;
            }
            QTableWidget::item {
                padding: 15px 12px;
                color: #2d3748;
                border-bottom: 1px solid #f0f2f5;
            }
            QTableWidget::item:selected {
                background-color: #ebf8ff;
                color: #2c5282;
            }
            QTableWidget::item:hover {
                background-color: #f7fafc;
            }
        """)

        # configurar comportamiento de la tabla
        self.tabla_usuarios.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_usuarios.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_usuarios.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_usuarios.setAlternatingRowColors(False)
        self.tabla_usuarios.setShowGrid(True)

        # configurar headers horizontales para ocupar todo el ancho
        h_header = self.tabla_usuarios.horizontalHeader()
        if h_header:
            h_header.setSectionResizeMode(QHeaderView.Stretch)

        # configurar headers verticales
        v_header = self.tabla_usuarios.verticalHeader()
        if v_header:
            v_header.setVisible(False)
            # agregar más altura a las filas para mejor legibilidad
            v_header.setDefaultSectionSize(50)

        # doble-click en una fila abre el formulario de edición
        self.tabla_usuarios.doubleClicked.connect(self._editar_usuario_seleccionado)

        lista_layout.addWidget(self.tabla_usuarios)

        # ocultar el widget inicialmente
        self.lista_usuarios_widget.hide()

    def _create_stat_card(self, title, value, color):
        # crear una tarjeta de estadística con diseño moderno
        card = QWidget()
        card.setFixedHeight(100)
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 1px solid #e2e8f0;
                border-left: 4px solid {color};
                border-radius: 8px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 15, 20, 15)
        card_layout.setSpacing(8)

        # etiqueta del valor (número grande)
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: bold;
            color: {color};
        """)
        card_layout.addWidget(value_label)

        # etiqueta del título
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 13px;
            color: #718096;
            font-weight: 500;
        """)
        card_layout.addWidget(title_label)

        # guardar referencia al label del valor para actualizarlo después
        card.value_label = value_label

        return card

    def _cargar_tabla_usuarios(self):
        # cargar todos los usuarios desde la BD y mostrarlos en la tabla
        try:
            usuarios = self._usuario_service._repo.find_all()

            # actualizar estadísticas
            total_usuarios = len(usuarios)
            usuarios_activos = sum(1 for u in usuarios if u.activo == 1)
            usuarios_inactivos = total_usuarios - usuarios_activos

            self.card_total_usuarios.value_label.setText(str(total_usuarios))
            self.card_usuarios_activos.value_label.setText(str(usuarios_activos))
            self.card_usuarios_inactivos.value_label.setText(str(usuarios_inactivos))

            # limpiar la tabla antes de llenarla
            self.tabla_usuarios.setRowCount(0)

            # agregar cada usuario como una fila en la tabla
            for usuario in usuarios:
                row_position = self.tabla_usuarios.rowCount()
                self.tabla_usuarios.insertRow(row_position)

                # columna ID
                self.tabla_usuarios.setItem(row_position, 0, QTableWidgetItem(str(usuario.usuario_id)))

                # columna Nombre Completo
                nombre_completo = f"{usuario.nombre} {usuario.apellido_paterno}"
                if usuario.apellido_materno:
                    nombre_completo += f" {usuario.apellido_materno}"
                self.tabla_usuarios.setItem(row_position, 1, QTableWidgetItem(nombre_completo))

                # columna Email
                self.tabla_usuarios.setItem(row_position, 2, QTableWidgetItem(usuario.email))

                # columna Teléfono
                telefono = usuario.telefono if usuario.telefono else "N/A"
                self.tabla_usuarios.setItem(row_position, 3, QTableWidgetItem(telefono))

                # columna Rol
                self.tabla_usuarios.setItem(row_position, 4, QTableWidgetItem(usuario.nombre_rol))

                # columna Estado
                estado = "Activo" if usuario.activo == 1 else "Inactivo"
                item_estado = QTableWidgetItem(estado)
                # colorear según el estado
                if usuario.activo == 1:
                    item_estado.setForeground(QColor(34, 139, 34))  # verde oscuro
                else:
                    item_estado.setForeground(QColor(220, 53, 69))  # rojo
                self.tabla_usuarios.setItem(row_position, 5, item_estado)

                # columna Fecha Registro
                fecha = usuario.fecha_creacion if usuario.fecha_creacion else "N/A"
                self.tabla_usuarios.setItem(row_position, 6, QTableWidgetItem(fecha))


        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudieron cargar los usuarios: {str(e)}"
            )

    def _mostrar_seccion_usuarios(self):
        # mostrar la lista de usuarios y ocultar otras vistas
        self._ocultar_contenido_actual()

        # agregar y mostrar la lista de usuarios
        if self.lista_usuarios_widget.parent() != self.contentArea:
            self.contentLayout.addWidget(self.lista_usuarios_widget)

        self.lista_usuarios_widget.show()
        self.headerPageTitle.setText("Usuarios")

        # cargar los datos de la tabla
        self._cargar_tabla_usuarios()

        # resaltar el botón de Usuarios en el sidebar
        if hasattr(self, 'btnUsuarios'):
            self._resaltar_boton_activo(self.btnUsuarios)

    def _mostrar_form_nuevo_usuario(self):
        # resetear modo edición
        self._usuario_editando = None
        self._ocultar_contenido_actual()

        if self.form_usuarios_widget.parent() != self.contentArea:
            self.contentLayout.addWidget(self.form_usuarios_widget)

        self.form_usuarios_widget.show()
        self.headerPageTitle.setText("Usuarios - Nuevo")
        self.form_titulo.setText("Nuevo Usuario")
        self.form_subtitulo.setText(
            "Completa la información del nuevo usuario del sistema. "
            "Los campos marcados con * son obligatorios."
        )
        self.btn_guardar.setText("Guardar Usuario")
        self.label_password.setText("Contraseña *")
        self.label_confirm_password.setText("Confirmar Contraseña *")
        self._limpiar_formulario()

    def _editar_usuario_seleccionado(self, index):
        # obtener el ID del usuario desde la fila seleccionada
        row = index.row()
        usuario_id_item = self.tabla_usuarios.item(row, 0)
        if not usuario_id_item:
            return

        usuario_id = int(usuario_id_item.text())

        # buscar el usuario completo en la lista cargada
        try:
            usuarios = self._usuario_service._repo.find_all()
            usuario = next((u for u in usuarios if u.usuario_id == usuario_id), None)
            if not usuario:
                return
        except Exception:
            return

        self._usuario_editando = usuario
        self._ocultar_contenido_actual()

        if self.form_usuarios_widget.parent() != self.contentArea:
            self.contentLayout.addWidget(self.form_usuarios_widget)

        self.form_usuarios_widget.show()
        self.headerPageTitle.setText("Usuarios - Editar")
        self.form_titulo.setText("Editar Usuario")
        self.form_subtitulo.setText(
            f"Editando usuario: {usuario.nombre} {usuario.apellido_paterno}. "
            "Deja los campos de contraseña vacíos para mantener la actual."
        )
        self.btn_guardar.setText("Actualizar Usuario")
        self.label_password.setText("Nueva Contraseña")
        self.label_confirm_password.setText("Confirmar Nueva Contraseña")

        # poblar el formulario con los datos del usuario
        self.input_nombre.setText(usuario.nombre)
        self.input_apellido_paterno.setText(usuario.apellido_paterno)
        self.input_apellido_materno.setText(usuario.apellido_materno or "")
        self.input_email.setText(usuario.email)
        self.input_telefono.setText(usuario.telefono or "")
        self.input_password.clear()
        self.input_confirm_password.clear()
        self.check_activo.setChecked(usuario.activo == 1)

        # seleccionar el rol correcto en el combo
        for i in range(self.combo_rol.count()):
            if self.combo_rol.itemData(i) == usuario.rol_id:
                self.combo_rol.setCurrentIndex(i)
                break

    def _ocultar_contenido_actual(self):
        # ocultar todos los widgets y spacers del área de contenido
        for i in range(self.contentLayout.count()):
            item = self.contentLayout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.hide()
            elif item.spacerItem():
                item.spacerItem().changeSize(0, 0)
            elif item.layout():
                # ocultar widgets dentro de sub-layouts (ej: cardsRow)
                for j in range(item.layout().count()):
                    sub_widget = item.layout().itemAt(j).widget()
                    if sub_widget:
                        sub_widget.hide()
        self.contentLayout.invalidate()

    def _create_form_usuarios(self):
        # crear el widget de formulario de alta de usuarios con diseño mejorado
        self.form_usuarios_widget = QWidget()
        form_layout = QVBoxLayout(self.form_usuarios_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # crear un scroll area para el formulario
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")

        # contenedor del formulario
        form_container = QWidget()
        container_layout = QVBoxLayout(form_container)
        container_layout.setSpacing(30)
        container_layout.setContentsMargins(0, 0, 20, 0)

        # cabecera del formulario
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        self.form_titulo = QLabel("Nuevo Usuario")
        self.form_titulo.setStyleSheet("font-size: 32px; font-weight: bold; color: #1a1a2e;")
        header_layout.addWidget(self.form_titulo)

        self.form_subtitulo = QLabel("Completa la información del nuevo usuario del sistema. Los campos marcados con * son obligatorios.")
        self.form_subtitulo.setStyleSheet("font-size: 15px; color: #718096; line-height: 1.5;")
        self.form_subtitulo.setWordWrap(True)
        header_layout.addWidget(self.form_subtitulo)

        container_layout.addWidget(header_container)

        # contenedor con fondo blanco para el formulario
        form_card = QWidget()
        form_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        form_card_layout = QVBoxLayout(form_card)
        form_card_layout.setContentsMargins(40, 35, 40, 35)
        form_card_layout.setSpacing(25)

        # crear el grid para los campos del formulario con diseño de 2 columnas
        form_grid = QGridLayout()
        form_grid.setHorizontalSpacing(25)
        form_grid.setVerticalSpacing(20)
        form_grid.setColumnStretch(1, 1)
        form_grid.setColumnStretch(3, 1)

        # estilos mejorados para los inputs
        input_style = """
            QLineEdit, QComboBox {
                padding: 14px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: #f7fafc;
                font-size: 15px;
                min-height: 48px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #4a90d9;
                background-color: white;
            }
            QLineEdit:hover, QComboBox:hover {
                border: 2px solid #cbd5e0;
            }
        """

        label_style = """
            font-size: 14px;
            color: #2d3748;
            font-weight: 600;
        """

        row = 0

        # sección de información personal
        seccion_personal = QLabel("Información Personal")
        seccion_personal.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a1a2e; margin-top: 5px;")
        form_grid.addWidget(seccion_personal, row, 0, 1, 4)
        row += 1

        # nombre (columna izquierda)
        nombre_layout = QVBoxLayout()
        nombre_layout.setSpacing(8)
        label_nombre = QLabel("Nombre *")
        label_nombre.setStyleSheet(label_style)
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingresa el nombre")
        self.input_nombre.setStyleSheet(input_style)
        nombre_layout.addWidget(label_nombre)
        nombre_layout.addWidget(self.input_nombre)
        form_grid.addLayout(nombre_layout, row, 0)

        # apellido paterno (columna derecha)
        apellido_p_layout = QVBoxLayout()
        apellido_p_layout.setSpacing(8)
        label_apellido_p = QLabel("Apellido Paterno *")
        label_apellido_p.setStyleSheet(label_style)
        self.input_apellido_paterno = QLineEdit()
        self.input_apellido_paterno.setPlaceholderText("Ingresa el apellido paterno")
        self.input_apellido_paterno.setStyleSheet(input_style)
        apellido_p_layout.addWidget(label_apellido_p)
        apellido_p_layout.addWidget(self.input_apellido_paterno)
        form_grid.addLayout(apellido_p_layout, row, 1)
        row += 1

        # apellido materno (columna izquierda)
        apellido_m_layout = QVBoxLayout()
        apellido_m_layout.setSpacing(8)
        label_apellido_m = QLabel("Apellido Materno")
        label_apellido_m.setStyleSheet(label_style)
        self.input_apellido_materno = QLineEdit()
        self.input_apellido_materno.setPlaceholderText("Ingresa el apellido materno (opcional)")
        self.input_apellido_materno.setStyleSheet(input_style)
        apellido_m_layout.addWidget(label_apellido_m)
        apellido_m_layout.addWidget(self.input_apellido_materno)
        form_grid.addLayout(apellido_m_layout, row, 0)

        # teléfono (columna derecha)
        telefono_layout = QVBoxLayout()
        telefono_layout.setSpacing(8)
        label_telefono = QLabel("Teléfono")
        label_telefono.setStyleSheet(label_style)
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("10 dígitos (opcional)")
        self.input_telefono.setMaxLength(10)
        self.input_telefono.setStyleSheet(input_style)
        telefono_layout.addWidget(label_telefono)
        telefono_layout.addWidget(self.input_telefono)
        form_grid.addLayout(telefono_layout, row, 1)
        row += 1

        # sección de cuenta
        seccion_cuenta = QLabel("Información de Cuenta")
        seccion_cuenta.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a1a2e; margin-top: 15px;")
        form_grid.addWidget(seccion_cuenta, row, 0, 1, 4)
        row += 1

        # email (span completo)
        email_layout = QVBoxLayout()
        email_layout.setSpacing(8)
        label_email = QLabel("Email *")
        label_email.setStyleSheet(label_style)
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("ejemplo@correo.com")
        self.input_email.setStyleSheet(input_style)
        email_layout.addWidget(label_email)
        email_layout.addWidget(self.input_email)
        form_grid.addLayout(email_layout, row, 0, 1, 2)
        row += 1

        # contraseña (columna izquierda)
        password_main_layout = QVBoxLayout()
        password_main_layout.setSpacing(8)
        self.label_password = QLabel("Contraseña *")
        self.label_password.setStyleSheet(label_style)

        password_container = QWidget()
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(8)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Mínimo 8 caracteres")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet(input_style)

        self.btn_toggle_password = QPushButton("👁")
        self.btn_toggle_password.setFixedSize(48, 48)
        self.btn_toggle_password.setStyleSheet("""
            QPushButton {
                background-color: #f0f2f5;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                border: 2px solid #cbd5e0;
            }
        """)
        self.btn_toggle_password.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_toggle_password.clicked.connect(self._toggle_password_visibility)

        password_layout.addWidget(self.input_password)
        password_layout.addWidget(self.btn_toggle_password)

        password_main_layout.addWidget(self.label_password)
        password_main_layout.addWidget(password_container)
        form_grid.addLayout(password_main_layout, row, 0)

        # confirmar contraseña (columna derecha)
        confirm_main_layout = QVBoxLayout()
        confirm_main_layout.setSpacing(8)
        self.label_confirm_password = QLabel("Confirmar Contraseña *")
        self.label_confirm_password.setStyleSheet(label_style)

        confirm_password_container = QWidget()
        confirm_password_layout = QHBoxLayout(confirm_password_container)
        confirm_password_layout.setContentsMargins(0, 0, 0, 0)
        confirm_password_layout.setSpacing(8)

        self.input_confirm_password = QLineEdit()
        self.input_confirm_password.setPlaceholderText("Repite la contraseña")
        self.input_confirm_password.setEchoMode(QLineEdit.Password)
        self.input_confirm_password.setStyleSheet(input_style)

        self.btn_toggle_confirm = QPushButton("👁")
        self.btn_toggle_confirm.setFixedSize(48, 48)
        self.btn_toggle_confirm.setStyleSheet("""
            QPushButton {
                background-color: #f0f2f5;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                border: 2px solid #cbd5e0;
            }
        """)
        self.btn_toggle_confirm.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_toggle_confirm.clicked.connect(self._toggle_confirm_visibility)

        confirm_password_layout.addWidget(self.input_confirm_password)
        confirm_password_layout.addWidget(self.btn_toggle_confirm)

        confirm_main_layout.addWidget(self.label_confirm_password)
        confirm_main_layout.addWidget(confirm_password_container)
        form_grid.addLayout(confirm_main_layout, row, 1)
        row += 1

        # sección de permisos
        seccion_permisos = QLabel("Permisos y Estado")
        seccion_permisos.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a1a2e; margin-top: 15px;")
        form_grid.addWidget(seccion_permisos, row, 0, 1, 4)
        row += 1

        # rol (columna izquierda)
        rol_layout = QVBoxLayout()
        rol_layout.setSpacing(8)
        label_rol = QLabel("Rol *")
        label_rol.setStyleSheet(label_style)
        self.combo_rol = QComboBox()
        self.combo_rol.setStyleSheet(input_style)
        self._cargar_roles()
        rol_layout.addWidget(label_rol)
        rol_layout.addWidget(self.combo_rol)
        form_grid.addLayout(rol_layout, row, 0)

        # estado (columna derecha)
        estado_layout = QVBoxLayout()
        estado_layout.setSpacing(8)
        label_activo = QLabel("Estado")
        label_activo.setStyleSheet(label_style)
        self.check_activo = QCheckBox("Usuario activo")
        self.check_activo.setChecked(True)
        self.check_activo.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                color: #2d3748;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #e2e8f0;
                border-radius: 4px;
                background-color: #f7fafc;
            }
            QCheckBox::indicator:checked {
                background-color: #4a90d9;
                border-color: #4a90d9;
                image: url(none);
            }
            QCheckBox::indicator:hover {
                border-color: #cbd5e0;
            }
        """)
        estado_layout.addWidget(label_activo)
        estado_layout.addWidget(self.check_activo)
        form_grid.addLayout(estado_layout, row, 1)
        row += 1

        # agregar el grid a la tarjeta
        form_card_layout.addLayout(form_grid)

        container_layout.addWidget(form_card)

        # botones de acción fuera de la tarjeta
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(0, 10, 0, 0)

        self.btn_guardar = QPushButton("Guardar Usuario")
        self.btn_guardar.setFixedSize(180, 55)
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #4a90d9;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3a7bc8;
            }
            QPushButton:pressed {
                background-color: #2a6bb8;
            }
        """)
        self.btn_guardar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_guardar.clicked.connect(self._guardar_usuario)

        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setFixedSize(120, 55)
        self.btn_limpiar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2d3748;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f7fafc;
                border-color: #cbd5e0;
            }
        """)
        self.btn_limpiar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_limpiar.clicked.connect(self._limpiar_formulario)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setFixedSize(120, 55)
        self.btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #718096;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f7fafc;
                border-color: #cbd5e0;
            }
        """)
        self.btn_cancelar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_cancelar.clicked.connect(self._mostrar_seccion_usuarios)

        buttons_layout.addWidget(self.btn_guardar)
        buttons_layout.addWidget(self.btn_limpiar)
        buttons_layout.addWidget(self.btn_cancelar)
        buttons_layout.addStretch()

        container_layout.addLayout(buttons_layout)
        container_layout.addStretch()

        # configurar el scroll area
        scroll.setWidget(form_container)
        form_layout.addWidget(scroll)

        # ocultar el formulario inicialmente - se mostrará cuando se presione "Nuevo Usuario"
        self.form_usuarios_widget.hide()

    def _cargar_roles(self):
        # cargar los roles desde la base de datos y llenar el combobox
        try:
            roles = self._rol_repository.find_all()
            for rol in roles:
                self.combo_rol.addItem(rol.nombre_rol, rol.rol_id)
        except Exception as e:
            # si hay error al cargar roles, mostrar mensaje
            QMessageBox.warning(
                self,
                "Error",
                f"No se pudieron cargar los roles: {str(e)}"
            )

    def _toggle_password_visibility(self):
        # alternar entre mostrar y ocultar la contraseña
        if self.input_password.echoMode() == QLineEdit.Password:
            self.input_password.setEchoMode(QLineEdit.Normal)
            self.btn_toggle_password.setText("🙈")
        else:
            self.input_password.setEchoMode(QLineEdit.Password)
            self.btn_toggle_password.setText("👁")

    def _toggle_confirm_visibility(self):
        # alternar entre mostrar y ocultar la confirmación de contraseña
        if self.input_confirm_password.echoMode() == QLineEdit.Password:
            self.input_confirm_password.setEchoMode(QLineEdit.Normal)
            self.btn_toggle_confirm.setText("🙈")
        else:
            self.input_confirm_password.setEchoMode(QLineEdit.Password)
            self.btn_toggle_confirm.setText("👁")

    def _validar_formulario(self):
        # validar que todos los campos requeridos estén completos
        if not self.input_nombre.text().strip():
            return False, "El nombre es requerido"

        if not self.input_apellido_paterno.text().strip():
            return False, "El apellido paterno es requerido"

        if not self.input_email.text().strip():
            return False, "El email es requerido"

        # en modo crear, la contraseña es obligatoria
        # en modo editar, solo se valida si se escribió algo
        contrasena = self.input_password.text()
        confirmar = self.input_confirm_password.text()
        es_edicion = self._usuario_editando is not None

        if not es_edicion:
            if not contrasena:
                return False, "La contraseña es requerida"
            if not confirmar:
                return False, "Debes confirmar la contraseña"

        if contrasena or confirmar:
            if contrasena != confirmar:
                return False, "Las contraseñas no coinciden"
            if len(contrasena) < 8:
                return False, "La contraseña debe tener al menos 8 caracteres"

        # validar formato de teléfono si se proporciona
        telefono = self.input_telefono.text().strip()
        if telefono and (not telefono.isdigit() or len(telefono) != 10):
            return False, "El teléfono debe contener exactamente 10 dígitos"

        return True, None

    def _guardar_usuario(self):
        # validar el formulario antes de guardar
        valido, mensaje_error = self._validar_formulario()
        if not valido:
            QMessageBox.warning(self, "Error de Validación", mensaje_error)
            return

        # recopilar los datos del formulario
        datos_usuario = {
            "nombre": self.input_nombre.text().strip(),
            "apellido_paterno": self.input_apellido_paterno.text().strip(),
            "apellido_materno": self.input_apellido_materno.text().strip(),
            "email": self.input_email.text().strip(),
            "telefono": self.input_telefono.text().strip(),
            "contrasena": self.input_password.text(),
            "rol_id": self.combo_rol.currentData(),
            "activo": 1 if self.check_activo.isChecked() else 0,
        }

        if self._usuario_editando:
            # modo edición
            usuario, error = self._usuario_service.actualizar_usuario(
                self._usuario_editando.usuario_id, datos_usuario
            )
            titulo_error = "Error al Actualizar Usuario"
            titulo_exito = "Usuario Actualizado"
            msg_exito = "ha sido actualizado exitosamente."
        else:
            # modo creación
            usuario, error = self._usuario_service.crear_usuario(datos_usuario)
            titulo_error = "Error al Crear Usuario"
            titulo_exito = "Usuario Creado"
            msg_exito = "ha sido creado exitosamente."

        if error:
            QMessageBox.critical(self, titulo_error, error)
        elif usuario:
            nombre_completo = f"{usuario.nombre} {usuario.apellido_paterno}"
            QMessageBox.information(
                self,
                titulo_exito,
                f"El usuario {nombre_completo} {msg_exito}"
            )
            self._mostrar_seccion_usuarios()

    def _limpiar_formulario(self):
        # limpiar todos los campos del formulario
        self.input_nombre.clear()
        self.input_apellido_paterno.clear()
        self.input_apellido_materno.clear()
        self.input_email.clear()
        self.input_telefono.clear()
        self.input_password.clear()
        self.input_confirm_password.clear()
        self.combo_rol.setCurrentIndex(0)
        self.check_activo.setChecked(True)
        # enfocar el primer campo
        self.input_nombre.setFocus()
