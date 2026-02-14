# Dialog generico para crear/editar registros de cualquier catalogo

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QDoubleSpinBox, QPushButton, QFrame, QColorDialog,
    QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from app.repositories.catalogo_repository import CatalogoRepository


DIALOG_STYLE = """
QDialog {
    background-color: white;
}
QLabel.fieldLabel {
    font-size: 13px;
    color: #2d3748;
    font-weight: 600;
}
QLabel#dialogTitle {
    font-size: 18px;
    font-weight: bold;
    color: #1a1a2e;
}
QLineEdit, QComboBox {
    padding: 8px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    background-color: #f7fafc;
    font-size: 13px;
    min-height: 34px;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #4a90d9;
    background-color: white;
}
QLineEdit:hover, QComboBox:hover {
    border: 1px solid #cbd5e0;
}
QSpinBox, QDoubleSpinBox {
    padding: 8px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    background-color: #f7fafc;
    font-size: 13px;
    min-height: 34px;
}
QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #4a90d9;
    background-color: white;
}
QPushButton#btnGuardar {
    background-color: #4a90d9;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    padding: 10px 24px;
    min-height: 38px;
}
QPushButton#btnGuardar:hover {
    background-color: #3a7bc8;
}
QPushButton#btnCancelar {
    background-color: white;
    color: #2d3748;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    padding: 10px 20px;
    min-height: 38px;
}
QPushButton#btnCancelar:hover {
    background-color: #f7fafc;
    border-color: #cbd5e0;
}
QPushButton.colorBtn {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    min-height: 34px;
    min-width: 60px;
    font-size: 13px;
}
QPushButton.colorBtn:hover {
    border-color: #cbd5e0;
}
"""


class CatalogoFormDialog(QDialog):

    def __init__(self, config, datos_edicion=None, parent=None):
        super().__init__(parent)
        self._config = config
        self._datos_edicion = datos_edicion
        self._inputs = {}
        self._setup_ui()

    def _setup_ui(self):
        singular = self._config.get('display_name_singular', 'Registro')
        if self._datos_edicion:
            self.setWindowTitle(f"Editar {singular}")
        else:
            self.setWindowTitle(f"Nuevo {singular}")

        self.setMinimumWidth(420)
        self.setStyleSheet(DIALOG_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        # titulo
        title = QLabel(self.windowTitle())
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        # separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #e2e8f0;")
        layout.addWidget(sep)

        # campos dinamicos
        for col_config in self._config['columns']:
            col_name = col_config['name']
            col_label = col_config['label']
            col_type = col_config.get('type', 'text')
            required = col_config.get('required', False)

            label_text = f"{col_label} *" if required else col_label
            label = QLabel(label_text)
            label.setProperty("class", "fieldLabel")
            label.setStyleSheet("font-size: 13px; color: #2d3748; font-weight: 600;")
            layout.addWidget(label)

            if col_type == 'text':
                widget = QLineEdit()
                widget.setPlaceholderText(f"Ingresa {col_label.lower()}")
                if self._datos_edicion:
                    val = getattr(self._datos_edicion, col_name, '')
                    widget.setText(str(val) if val else '')
                self._inputs[col_name] = widget
                layout.addWidget(widget)

            elif col_type == 'int':
                widget = QSpinBox()
                widget.setRange(0, 999999)
                if self._datos_edicion:
                    val = getattr(self._datos_edicion, col_name, 0)
                    widget.setValue(int(val) if val else 0)
                self._inputs[col_name] = widget
                layout.addWidget(widget)

            elif col_type == 'float':
                widget = QDoubleSpinBox()
                widget.setRange(0.0, 100.0)
                widget.setDecimals(2)
                widget.setSuffix(" %")
                if self._datos_edicion:
                    val = getattr(self._datos_edicion, col_name, 0.0)
                    widget.setValue(float(val) if val else 0.0)
                self._inputs[col_name] = widget
                layout.addWidget(widget)

            elif col_type == 'color':
                row_layout = QHBoxLayout()
                line_edit = QLineEdit()
                line_edit.setPlaceholderText("#000000")
                color_preview = QFrame()
                color_preview.setFixedSize(34, 34)
                color_preview.setStyleSheet(
                    "background-color: #cccccc; border: 1px solid #e2e8f0; border-radius: 6px;"
                )
                btn_color = QPushButton("Elegir")
                btn_color.setProperty("class", "colorBtn")
                btn_color.setCursor(Qt.PointingHandCursor)
                btn_color.setStyleSheet(
                    "border: 1px solid #e2e8f0; border-radius: 6px; "
                    "min-height: 34px; min-width: 60px; font-size: 13px; "
                    "background-color: #f7fafc;"
                )

                def make_color_handler(le, preview):
                    def handler():
                        current = le.text().strip()
                        initial = QColor(current) if current else QColor("#cccccc")
                        color = QColorDialog.getColor(initial, self, "Seleccionar Color")
                        if color.isValid():
                            le.setText(color.name())
                            preview.setStyleSheet(
                                f"background-color: {color.name()}; "
                                "border: 1px solid #e2e8f0; border-radius: 6px;"
                            )
                    return handler

                btn_color.clicked.connect(make_color_handler(line_edit, color_preview))

                # actualizar preview cuando se escribe un color manualmente
                def make_text_handler(le, preview):
                    def handler(text):
                        c = QColor(text)
                        if c.isValid():
                            preview.setStyleSheet(
                                f"background-color: {c.name()}; "
                                "border: 1px solid #e2e8f0; border-radius: 6px;"
                            )
                    return handler

                line_edit.textChanged.connect(make_text_handler(line_edit, color_preview))

                if self._datos_edicion:
                    val = getattr(self._datos_edicion, col_name, '')
                    if val:
                        line_edit.setText(str(val))
                        color_preview.setStyleSheet(
                            f"background-color: {val}; "
                            "border: 1px solid #e2e8f0; border-radius: 6px;"
                        )

                row_layout.addWidget(line_edit)
                row_layout.addWidget(color_preview)
                row_layout.addWidget(btn_color)
                self._inputs[col_name] = line_edit
                layout.addLayout(row_layout)

            elif col_type == 'fk':
                widget = QComboBox()
                fk_config = col_config.get('fk_config')
                if fk_config:
                    fk_repo = CatalogoRepository(fk_config)
                    items = fk_repo.find_all()
                    display_col = fk_config['columns'][0]['name']
                    for item in items:
                        widget.addItem(getattr(item, display_col, ''), item.id)
                if self._datos_edicion:
                    val = getattr(self._datos_edicion, col_name, None)
                    if val:
                        for i in range(widget.count()):
                            if widget.itemData(i) == val:
                                widget.setCurrentIndex(i)
                                break
                self._inputs[col_name] = widget
                layout.addWidget(widget)

        # espaciador
        layout.addSpacing(8)

        # botones
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setObjectName("btnGuardar")
        btn_guardar.setCursor(Qt.PointingHandCursor)
        btn_guardar.clicked.connect(self.accept)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnCancelar")
        btn_cancelar.setCursor(Qt.PointingHandCursor)
        btn_cancelar.clicked.connect(self.reject)

        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def get_datos(self):
        datos = {}
        for col_config in self._config['columns']:
            col_name = col_config['name']
            widget = self._inputs.get(col_name)
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
