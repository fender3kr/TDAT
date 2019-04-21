# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TFAnnotatorDockWidget
                                 A QGIS plugin
 Tensorflow Dataset Annotation Tool
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-08-24
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Seokyong Hong
        email                : shong3@ncsu.edu
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
from __future__ import division

import os
import sys

from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QColor
from PyQt5.QtCore import pyqtSignal, QFileInfo
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QHeaderView
from qgis.utils import iface
from qgis.gui import QgsRubberBand
from qgis.core import QgsWkbTypes, QgsRasterLayer, QgsProject, QgsPointXY, QgsCoordinateReferenceSystem
from .util.Annotation import Annotation
from .util.ImageLoader import ImageLoader
from .util.PBTXTWriter import PBTXTWriter
from .util.TFUtil import _int64_feature, _bytes_feature, _bytes_list_feature, _int64_list_feature, _float_list_feature
from .tools.SelectMapTool import SelectMapTool
from .tools.InformationRetriever import InformationRetriever

import tensorflow as tflow

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tf_annotator_dockwidget_base.ui'))


class TFAnnotatorDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(TFAnnotatorDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # TF Annotation Tool UI Setup
        self.addLabelButton.clicked.connect(self.addLabelButtonClicked)
        self.deleteLabelButton.clicked.connect(self.deleteLabelButtonClicked)
        self.addAnnotationButton.clicked.connect(self.addAnnotationButtonClicked)
        self.deleteAnnotationButton.clicked.connect(self.deleteAnnotationButtonClicked)
        self.clearButton.clicked.connect(self.clearButtonClicked)
        self.exportButton.clicked.connect(self.exportButtonClicked)
        
        self.model = QStandardItemModel(self.annotationView)
        self.model.setHorizontalHeaderLabels(["Label", "Layer", "Path", "CRS", "Top", "Left", "Bottom", "Right", "C1X", "C1Y", "C2X", "C2Y"])
        self.annotationView.setModel(self.model)
        self.annotationView.selectionModel().selectionChanged.connect(self.currentRowChanged)
        self.annotationView.hideColumn(2)
        self.annotationView.hideColumn(4)
        self.annotationView.hideColumn(5)
        self.annotationView.hideColumn(6)
        self.annotationView.hideColumn(7)
        self.annotationView.hideColumn(8)
        self.annotationView.hideColumn(9)
        self.annotationView.hideColumn(10)
        self.annotationView.hideColumn(11)
        self.annotationView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.selectionBand = QgsRubberBand(iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
        self.selectionBand.setColor(QColor('green'))
        self.selectionBand.setWidth(1)

    def addLabelButtonClicked(self):
        self.resetSelectionBand()
        label = self.labelComboBox.currentText().strip()
        if self.labelComboBox.findText(label, QtCore.Qt.MatchExactly) < 0:
            self.labelComboBox.addItem(label)
        else:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText(label + " already exists.")
            messageBox.exec_()
        self.labelComboBox.setCurrentIndex(-1)

    def deleteLabelButtonClicked(self):
        self.resetSelectionBand()
        labelIndex = self.labelComboBox.currentIndex()
        if labelIndex >= 0:
            self.labelComboBox.removeItem(labelIndex)
        else:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Label is not selected.")
            messageBox.exec_()

    def addAnnotationButtonClicked(self):
        self.resetSelectionBand()
        labelIndex = self.labelComboBox.currentIndex()
        if labelIndex < 0:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Label is not selected.")
            messageBox.exec_()
            return;
        
        currentMapTool = iface.mapCanvas().mapTool()
        if not isinstance(currentMapTool, SelectMapTool):
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Object is not selected.")
            messageBox.exec_()
            return;
                        
        if not currentMapTool.isValid():
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Selection is not valid.")
            messageBox.exec_()
            return;
        
        information = currentMapTool.getInformation()
        if information is None:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Information cannot be retrieved.")
            messageBox.exec_()
            return;
        
        crs = information.getCRS()
        
        aY, aX, bY, bX = information.getAbsoluteSelection()
        c1, c2 = information.getCoordinates()
        
        file = QFileInfo(information.getDataSource())
        row = [self.labelComboBox.currentText(), file.baseName(), file.filePath(), crs.authid(), str(aY), str(aX), str(bY), str(bX), str(c1.x()), str(c1.y()), str(c2.x()), str(c2.y())]
        self.model.appendRow([QStandardItem(item) for item in row])
        currentMapTool.reset()
        
    def deleteAnnotationButtonClicked(self):
        indexes = self.annotationView.selectedIndexes()
        if len(indexes) == 0:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Annotation is not selected.")
            messageBox.exec_()
            return

        self.model.takeRow(indexes[0].row())
        self.resetSelectionBand()

    def currentRowChanged(self, selected, deselected):
        indexes = self.annotationView.selectedIndexes()
        if len(indexes) == 0:
            return

        rowIndex = indexes[0].row()
        targetLayer = None
        
        for node in QgsProject.instance().layerTreeRoot().findLayers():
            layer = node.layer()
            if isinstance(layer, QgsRasterLayer) and layer.dataProvider().dataSourceUri() == self.model.item(rowIndex, 2).text():
                targetLayer = layer
                break

        root = QgsProject.instance().layerTreeRoot()
        if targetLayer is None:
            file = QFileInfo(self.model.item(rowIndex, 2).text())
            path = file.filePath()
            base = file.baseName()
            targetLayer = QgsRasterLayer(path, base)
            QgsProject.instance().addMapLayer(targetLayer, False)
            root.insertLayer(0, targetLayer)
        else:
            clonedLayer = targetLayer.clone()
            QgsProject.instance().removeMapLayer(targetLayer.id())
            QgsProject.instance().addMapLayer(clonedLayer)
            targetLayer = clonedLayer

        iface.setActiveLayer(targetLayer)
        crs = QgsCoordinateReferenceSystem(self.model.item(rowIndex, 3).text())
        QgsProject.instance().setCrs(crs)
        iface.mapCanvas().setExtent(targetLayer.extent())
        
        point1 = QgsPointXY(float(self.model.item(rowIndex, 8).text()), float(self.model.item(rowIndex, 9).text()))
        point2 = QgsPointXY(float(self.model.item(rowIndex, 8).text()), float(self.model.item(rowIndex, 11).text()))
        point3 = QgsPointXY(float(self.model.item(rowIndex, 10).text()), float(self.model.item(rowIndex, 11).text()))
        point4 = QgsPointXY(float(self.model.item(rowIndex, 10).text()), float(self.model.item(rowIndex, 9).text()))
        
        self.resetSelectionBand()
        self.selectionBand.addPoint(point1, False)
        self.selectionBand.addPoint(point2, False)
        self.selectionBand.addPoint(point3, False)
        self.selectionBand.addPoint(point4, True)
        
        self.selectionBand.setOpacity(0.5)
        self.selectionBand.show()

    def clearButtonClicked(self):
        currentMapTool = iface.mapCanvas().mapTool()
        if isinstance(currentMapTool, SelectMapTool):
            currentMapTool.reset()
        
        self.model.removeRows(0, self.model.rowCount())
        self.resetSelectionBand()

    def exportButtonClicked(self):
        self.resetSelectionBand()
        
        if self.model.rowCount() == 0:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("There is no annotation.")
            messageBox.exec_()
            return

        path, _ = QFileDialog.getSaveFileName(self, "TFRecord File", "", "TFRecord File (*.tfrecord)")
        if path == "":
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("File is not selected.")
            messageBox.exec_()
            return
        
        self.export(path)

    def closeEvent(self, event):
        self.resetSelectionBand()
        self.closingPlugin.emit()
        event.accept()
        
    def resetSelectionBand(self):
        self.selectionBand.reset(QgsWkbTypes.PolygonGeometry)
        
    def export(self, outputPath):
        annotations = {}
        
        for rowIndex in range(self.model.rowCount()):
            label = self.model.item(rowIndex, 0).text()
            # Label must start from 1 since Tensorflow internally use 0.
            labelIndex = self.labelComboBox.findText(label) + 1
            
            annotation = Annotation(self.model.item(rowIndex, 2).text(), int(self.model.item(rowIndex, 4).text()), int(self.model.item(rowIndex, 5).text()), int(self.model.item(rowIndex, 6).text()), int(self.model.item(rowIndex, 7).text()), int(labelIndex), label)            
            if annotation.path not in annotations:
                annotations[annotation.path] = []
            
            annotations[annotation.path].append(annotation)
        
        writer = tflow.python_io.TFRecordWriter(outputPath)
        index = 0
        for path in annotations:
            loader = ImageLoader(path)
            image, width, height = loader.load()
            basename = os.path.basename(path)
            xmins = []
            xmaxs = []
            ymins = []
            ymaxs = []
            classes_text = []
            classes = []
            
            for annotation in annotations[path]:
                xmins.append(annotation.left / width)
                xmaxs.append(annotation.right / width)
                ymins.append(annotation.top / height)
                ymaxs.append(annotation.bottom / height)
                classes_text.append(tflow.compat.as_bytes(annotation.label))
                classes.append(annotation.index)
            
            example = tflow.train.Example(features = tflow.train.Features(feature = {
                'image/width': _int64_feature(width),
                'image/height': _int64_feature(height),
                'image/filename': _bytes_feature(tflow.compat.as_bytes(basename)),
                'image/source_id': _bytes_feature(tflow.compat.as_bytes(basename)),
                'image/encoded': _bytes_feature(image),
                'image/format': _bytes_feature(tflow.compat.as_bytes('jpeg')),
                'image/object/bbox/xmin': _float_list_feature(xmins),
                'image/object/bbox/xmax': _float_list_feature(xmaxs),
                'image/object/bbox/ymin': _float_list_feature(ymins),
                'image/object/bbox/ymax': _float_list_feature(ymaxs),
                'image/object/class/text': _bytes_list_feature(classes_text),
                'image/object/class/label': _int64_list_feature(classes)
            }))
            writer.write(example.SerializeToString())
        
        writer.close()

        directory, file = os.path.split(outputPath)
        filename = os.path.splitext(file)[0]
        pbtxtPath = os.path.join(directory, filename + '.pbtxt')
        
        writer = PBTXTWriter()
        writer.open(pbtxtPath)
        for index in range(self.labelComboBox.count()):
            # Label must start from 1 since Tensorflow internally use 0.
            writer.write(index + 1, self.labelComboBox.itemText(index))
        writer.close()

        sys.stdout.flush()