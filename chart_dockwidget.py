# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ChartDockWidget
                                 A QGIS plugin
 qml chart
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-01-16
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Oslandia
        email                : julien.cabieces@oslandia.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtChart import QChartView, QChart, QLineSeries, QVXYModelMapper
from qgis.gui import QgsAttributeTableModel
from qgis.core import QgsVectorLayerCache, QgsProject
from qgis.utils import iface

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'chart_dockwidget_base.ui'))

QML_FILE = os.path.join(
    os.path.dirname(__file__), 'chart.qml')

class ChartDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(ChartDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)


        project = QgsProject.instance()
        self._layers.addItem("")
        for layerid, layer in project.mapLayers().items():
            self._layers.addItem(layer.sourceName(), layerid)

        self._layers.currentIndexChanged.connect(self.__on_layer_changed)
        self._axisX.currentIndexChanged.connect(self.__refresh_chart)
        self._axisY.currentIndexChanged.connect(self.__refresh_chart)

        chart = QChart()
        chartView = QChartView(chart, self)
        self._main.layout().addWidget(chartView)

        series = QLineSeries()
        series.setName("Line 1")
        self._mapper = QVXYModelMapper(chartView)
        self._mapper.setXColumn(0)
        self._mapper.setYColumn(2)
        self._mapper.setSeries(series)


        layer = iface.activeLayer()

        layer_cache = QgsVectorLayerCache(layer, 10000, chartView)
        layer_cache.setFullCache(True)

        model = QgsAttributeTableModel(layer_cache, chartView)
        model.loadLayer()
        
        self._mapper.setModel(model)
        chart.addSeries(series)
        
        #chart->setAnimationOptions(QChart::AllAnimations);

        
        
        # QML Stuff
        
        # self._quickWidget.setSource(QUrl(QML_FILE))

        # print("coucou={}".format(self._quickWidget.rootObject().objectName()))
        # print("test={}".format(self._quickWidget.rootObject().childItems()))
        # print("series={}".format(self._quickWidget.rootObject().series("LineSeries")))
        # for i in self._quickWidget.rootObject().childItems():
        #     print("i={}".format(i))

        # # line_series = self._quickWidget.rootObject().findChild(QLineSeries)
        # # line_series.setProperty("name", "tutu")

    def __on_layer_changed(self, index):

        layerid = self._layers.itemData(index)
        layer = QgsProject.instance().mapLayer(layerid)

        self._axisX.clear()
        self._axisX.addItems([""] + layer.fields().names())
        self._axisY.clear()
        self._axisY.addItems([""] + layer.fields().names())
        
    def __refresh_chart(self):

        pass
        # layerid = self._layers.itemData(self._layers.currentIndex())
        # layer = QgsProject.instance().mapLayer(layerid)

        # if layer and self._axisY and self._axisX:
        #     print("tutu x={} y={}".format(layer.fields().indexOf(self._axisX.currentText()), layer.fields().indexOf(self._axisY.currentText())))
        #     # self._mapper.setXColumn(layer.fields().indexOf(self._axisX.currentText()))
        #     # self._mapper.setYColumn(layer.fields().indexOf(self._axisY.currentText()))

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
