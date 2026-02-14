# Widget para listar y gestionar catalogos - carga .ui especifico por catalogo

import os
from PyQt5.QtWidgets import (
    QWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5 import uic
from app.services.catalogo_service import CatalogoService
from app.views.catalogo_form_dialog import CatalogoFormDialog

UI_DIR = os.path.join(os.path.dirname(__file__), "ui")


class CatalogoListWidget(QWidget):

    def __init__(self, config, parent=None):
        super().__init__(parent)

        # cargar el .ui especifico del catalogo
        ui_file = config.get('ui_list')
        ui_path = os.path.join(UI_DIR, ui_file)
        uic.loadUi(ui_path, self)

        self._config = config
        self._service = CatalogoService(config)
        self._items = []
        self._setup_ui()

    def _setup_ui(self):
        # conectar senales
        self.btnNuevo.clicked.connect(self._on_nuevo)
        self.tablaCatalogo.doubleClicked.connect(self._on_editar)

        # configurar headers de la tabla
        h_header = self.tablaCatalogo.horizontalHeader()
        h_header.setSectionResizeMode(QHeaderView.Stretch)

        col_count = self.tablaCatalogo.columnCount()

        # columna acciones mas pequena
        h_header.setSectionResizeMode(col_count - 1, QHeaderView.Fixed)
        self.tablaCatalogo.setColumnWidth(col_count - 1, 100)

        # columna ID mas pequena
        h_header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.tablaCatalogo.setColumnWidth(0, 60)

        v_header = self.tablaCatalogo.verticalHeader()
        v_header.setVisible(False)
        v_header.setDefaultSectionSize(42)

    def cargar_datos(self, filters=None):
        items, error = self._service.obtener_todos(filters)
        if error:
            QMessageBox.critical(self, "Error", error)
            return

        self._items = items
        self.statValue.setText(str(len(items)))
        self.tablaCatalogo.setRowCount(0)

        columns = self._config['columns']

        for item in items:
            row = self.tablaCatalogo.rowCount()
            self.tablaCatalogo.insertRow(row)

            # columna ID
            self.tablaCatalogo.setItem(row, 0, QTableWidgetItem(str(item.id)))

            # columnas de datos
            for col_idx, col_config in enumerate(columns):
                col_name = col_config['name']
                value = getattr(item, col_name, '')
                value_str = str(value) if value is not None else ''

                cell = QTableWidgetItem(value_str)

                # preview de color si es columna tipo color
                if col_config.get('type') == 'color' and value:
                    c = QColor(value)
                    if c.isValid():
                        cell.setForeground(c)
                        cell.setText(f"  {value}")

                self.tablaCatalogo.setItem(row, col_idx + 1, cell)

            # columna acciones: boton eliminar
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.setStyleSheet(
                "background-color: #f56565; color: white; border: none; "
                "border-radius: 4px; font-size: 12px; padding: 4px 12px; min-height: 28px;"
            )
            btn_eliminar.setCursor(Qt.PointingHandCursor)

            item_id = item.id
            btn_eliminar.clicked.connect(lambda checked, id_val=item_id: self._on_eliminar(id_val))

            self.tablaCatalogo.setCellWidget(row, len(columns) + 1, btn_eliminar)

    def _on_nuevo(self):
        dialog = CatalogoFormDialog(self._config, parent=self)
        if dialog.exec_() == CatalogoFormDialog.Accepted:
            datos = dialog.get_datos()
            result, error = self._service.crear(datos)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                self.cargar_datos()

    def _on_editar(self, index):
        row = index.row()
        id_item = self.tablaCatalogo.item(row, 0)
        if not id_item:
            return

        item_id = int(id_item.text())
        item, error = self._service.obtener_por_id(item_id)
        if error:
            QMessageBox.warning(self, "Error", error)
            return

        dialog = CatalogoFormDialog(self._config, datos_edicion=item, parent=self)
        if dialog.exec_() == CatalogoFormDialog.Accepted:
            datos = dialog.get_datos()
            result, error = self._service.actualizar(item_id, datos)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                self.cargar_datos()

    def _on_eliminar(self, item_id):
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminacion",
            "Estas seguro de que deseas eliminar este registro?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if respuesta == QMessageBox.Yes:
            result, error = self._service.eliminar(item_id)
            if error:
                QMessageBox.warning(self, "No se puede eliminar", error)
            else:
                self.cargar_datos()
