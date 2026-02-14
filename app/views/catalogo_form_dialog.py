# Dialog para crear/editar registros de catalogos - carga .ui especifico por catalogo

import os
from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QSpinBox, QDoubleSpinBox, QColorDialog, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5 import uic
from app.repositories.catalogo_repository import CatalogoRepository

UI_DIR = os.path.join(os.path.dirname(__file__), "ui")


class CatalogoFormDialog(QDialog):

    def __init__(self, config, datos_edicion=None, parent=None):
        super().__init__(parent)
        self._config = config
        self._datos_edicion = datos_edicion

        # cargar el .ui especifico del catalogo
        ui_file = config.get('ui_form')
        ui_path = os.path.join(UI_DIR, ui_file)
        uic.loadUi(ui_path, self)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # actualizar titulo si es edicion
        singular = config.get('display_name_singular', 'Registro')
        if datos_edicion:
            self.setWindowTitle(f"Editar {singular}")
            self.dialogTitle.setText(f"Editar {singular}")

        # conectar botones
        self.btnGuardar.clicked.connect(self.accept)
        self.btnCancelar.clicked.connect(self.reject)

        # conectar botones de color y poblar datos si es edicion
        self._setup_color_fields()
        self._setup_fk_fields()

        if datos_edicion:
            self._poblar_datos(datos_edicion)

    def _setup_color_fields(self):
        # conectar botones de color picker para campos tipo color
        for col_config in self._config['columns']:
            if col_config.get('type') != 'color':
                continue
            col_name = col_config['name']
            btn = getattr(self, f"btnColor_{col_name}", None)
            line_edit = getattr(self, f"input_{col_name}", None)
            preview = getattr(self, f"colorPreview_{col_name}", None)

            if btn and line_edit and preview:
                btn.clicked.connect(
                    self._make_color_handler(line_edit, preview)
                )
                line_edit.textChanged.connect(
                    self._make_text_handler(preview)
                )

    def _setup_fk_fields(self):
        # cargar opciones para campos tipo fk (foreign key)
        for col_config in self._config['columns']:
            if col_config.get('type') != 'fk':
                continue
            col_name = col_config['name']
            widget = getattr(self, f"input_{col_name}", None)
            if not isinstance(widget, QComboBox):
                continue

            fk_config = col_config.get('fk_config')
            if fk_config:
                fk_repo = CatalogoRepository(fk_config)
                items = fk_repo.find_all()
                display_col = fk_config['columns'][0]['name']
                for item in items:
                    widget.addItem(getattr(item, display_col, ''), item.id)

    def _make_color_handler(self, line_edit, preview):
        def handler():
            current = line_edit.text().strip()
            initial = QColor(current) if current else QColor("#cccccc")
            color = QColorDialog.getColor(initial, self, "Seleccionar Color")
            if color.isValid():
                line_edit.setText(color.name())
                preview.setStyleSheet(
                    f"background-color: {color.name()}; "
                    "border: 1px solid #e2e8f0; border-radius: 6px;"
                )
        return handler

    def _make_text_handler(self, preview):
        def handler(text):
            c = QColor(text)
            if c.isValid():
                preview.setStyleSheet(
                    f"background-color: {c.name()}; "
                    "border: 1px solid #e2e8f0; border-radius: 6px;"
                )
        return handler

    def _poblar_datos(self, datos):
        # poblar cada campo del formulario con los datos del registro
        for col_config in self._config['columns']:
            col_name = col_config['name']
            col_type = col_config.get('type', 'text')
            widget = getattr(self, f"input_{col_name}", None)
            if widget is None:
                continue

            val = getattr(datos, col_name, None)

            if isinstance(widget, QLineEdit):
                widget.setText(str(val) if val else '')
                if col_type == 'color' and val:
                    preview = getattr(self, f"colorPreview_{col_name}", None)
                    if preview:
                        preview.setStyleSheet(
                            f"background-color: {val}; "
                            "border: 1px solid #e2e8f0; border-radius: 6px;"
                        )
            elif isinstance(widget, QSpinBox):
                widget.setValue(int(val) if val else 0)
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(float(val) if val else 0.0)
            elif isinstance(widget, QComboBox):
                if val:
                    for i in range(widget.count()):
                        if widget.itemData(i) == val:
                            widget.setCurrentIndex(i)
                            break

    def get_datos(self):
        # recoger los datos de todos los campos del formulario
        datos = {}
        for col_config in self._config['columns']:
            col_name = col_config['name']
            widget = getattr(self, f"input_{col_name}", None)
            if widget is None:
                continue

            if isinstance(widget, QLineEdit):
                datos[col_name] = widget.text().strip()
            elif isinstance(widget, QSpinBox):
                datos[col_name] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                datos[col_name] = widget.value()
            elif isinstance(widget, QComboBox):
                datos[col_name] = widget.currentData()

        return datos
