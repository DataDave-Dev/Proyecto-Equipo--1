# Vista principal de Configuracion - tabs por categoria con sub-tabs para catalogos

import os
from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5 import uic
from app.config.catalogos import CATALOGO_CONFIGS, CATEGORIAS_ORDEN
from app.views.catalogo_list_widget import CatalogoListWidget
from app.views.geografia_widget import GeografiaWidget

UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "configuracion_view.ui")

# mapa de categoria -> objectName del sub-tab widget
CATEGORIA_OBJECT_NAMES = {
    'Ventas': 'ventasSubTabs',
    'Actividades': 'actividadesSubTabs',
    'Contactos': 'contactosSubTabs',
    'Finanzas': 'finanzasSubTabs',
}


class ConfiguracionView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(UI_PATH, self)
        self._catalog_widgets = {}
        self._setup_ui()

    def _setup_ui(self):
        self._populate_category_tabs()

    def _populate_category_tabs(self):
        # agrupar catalogos por categoria
        catalogos_por_categoria = {}
        for key, config in CATALOGO_CONFIGS.items():
            cat = config.get('category', 'Otros')
            if cat not in catalogos_por_categoria:
                catalogos_por_categoria[cat] = []
            catalogos_por_categoria[cat].append((key, config))

        # crear un tab por cada categoria
        for categoria in CATEGORIAS_ORDEN:
            if categoria == 'Geografia':
                # para geografia, mostrar el widget especializado directamente
                geo_widget = GeografiaWidget()
                self._catalog_widgets['__geografia__'] = geo_widget
                self.categoriasTabs.addTab(geo_widget, categoria)
                continue

            catalogos = catalogos_por_categoria.get(categoria, [])
            if not catalogos:
                continue

            # crear sub-tabs para los catalogos de esta categoria
            sub_tab_widget = QTabWidget()

            # asignar objectName especifico para los estilos CSS
            object_name = CATEGORIA_OBJECT_NAMES.get(categoria, 'genericSubTabs')
            sub_tab_widget.setObjectName(object_name)

            for key, config in catalogos:
                widget = CatalogoListWidget(config)
                self._catalog_widgets[key] = widget
                sub_tab_widget.addTab(widget, config['display_name'])

            # conectar señal de cambio de sub-tab
            sub_tab_widget.currentChanged.connect(
                lambda idx, w=sub_tab_widget: self._on_subtab_changed(w, idx)
            )

            self.categoriasTabs.addTab(sub_tab_widget, categoria)

        # conectar señal de cambio de tab principal
        self.categoriasTabs.currentChanged.connect(self._on_category_tab_changed)

        # cargar datos del primer tab
        if self.categoriasTabs.count() > 0:
            self._on_category_tab_changed(0)

    def _on_category_tab_changed(self, index):
        # cargar datos del widget actual cuando cambia el tab principal
        widget = self.categoriasTabs.widget(index)

        if isinstance(widget, GeografiaWidget):
            widget.cargar_datos()
        elif isinstance(widget, QTabWidget):
            # es un sub-tab, cargar el widget del sub-tab actual
            current_sub_widget = widget.currentWidget()
            if isinstance(current_sub_widget, CatalogoListWidget):
                current_sub_widget.cargar_datos()

    def _on_subtab_changed(self, sub_tab_widget, sub_index):
        # cargar datos cuando cambia el sub-tab
        widget = sub_tab_widget.widget(sub_index)
        if isinstance(widget, CatalogoListWidget):
            widget.cargar_datos()
