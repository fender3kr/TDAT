'''
Created on Aug 27, 2018

@author: Seokyong Hong
'''
import os.path
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox
from qgis.utils import iface
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsWkbTypes, QgsPointXY, QgsRectangle, QgsRasterLayer
from .InformationRetriever import InformationRetriever

class SelectMapTool(QgsMapTool):
    def __init__(self, canvas):
        super(SelectMapTool, self).__init__(canvas)
    
        self.rubberBand = QgsRubberBand(canvas, QgsWkbTypes.PolygonGeometry)
        self.rubberBand.setColor(QColor('orange'))
        self.rubberBand.setWidth(1)
        self.reset()
    
    def reset(self):
        self.start = self.end = None
        self.startCoordinate = self.endCoordinate = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        self.retriever = None
    
    def canvasPressEvent(self, event):
        self.start = event.pos()
        self.startCoordinate = self.toMapCoordinates(self.start)
        self.end = self.start 
        self.endCoordinate = self.startCoordinate
        self.isEmittingPoint = True
        self.showRect(self.startCoordinate, self.endCoordinate)
    
    def canvasReleaseEvent(self, event):
        self.isEmittingPoint = False
        
        if not isinstance(iface.activeLayer(), QgsRasterLayer):
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("The active layer is not raster.")
            messageBox.exec_()
            self.reset()
            return 
        
        rectangle = self.getRectangle()
        if rectangle is None:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Information)
            messageBox.setText("Object is not selected.")
            messageBox.exec_()
            self.reset()
            return
        
        self.retriever = InformationRetriever()
        self.retriever.retrieve(iface, self.start, self.end)
        self.retriever.setCoordinates(self.startCoordinate, self.endCoordinate)
        
    def canvasMoveEvent(self, event):
        if not self.isEmittingPoint:
            return
        
        self.end = event.pos()
        self.endCoordinate = self.toMapCoordinates(self.end)
        self.showRect(self.startCoordinate, self.endCoordinate)
    
    def showRect(self, startCoordinate, endCoordinate):
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        if startCoordinate.x() == endCoordinate.x() or startCoordinate.y() == endCoordinate.y():
            return
        
        point1 = QgsPointXY(startCoordinate.x(), startCoordinate.y())
        point2 = QgsPointXY(startCoordinate.x(), endCoordinate.y())
        point3 = QgsPointXY(endCoordinate.x(), endCoordinate.y())
        point4 = QgsPointXY(endCoordinate.x(), startCoordinate.y())
        
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)
        self.rubberBand.setOpacity(0.5)
        self.rubberBand.show()
    
    def getRectangle(self):
        if self.startCoordinate is None or self.endCoordinate is None:
            return None
        
        if self.startCoordinate.x() == self.endCoordinate.x() or self.startCoordinate.y() == self.endCoordinate.y():
            return None
        
        return QgsRectangle(self.startCoordinate, self.endCoordinate)
    
    def isValid(self):
        if self.retriever == None:
            return False
        
        if not isinstance(self.retriever.getLayer(), QgsRasterLayer):
            return False
        
        if iface.activeLayer() != self.retriever.getLayer():
            return False
        
        if not os.path.exists(self.retriever.getDataSource()):
            return False
        
        if self.retriever.getCRS().authid() != super().canvas().mapSettings().destinationCrs().authid():
            return False
        
        return True
    
    def getInformation(self):
        return self.retriever
    
    def deactivate(self):
        self.reset()