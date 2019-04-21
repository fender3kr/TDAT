'''
Created on Aug 28, 2018

@author: Seokyong Hong
'''
from math import floor
#from qgis.utils import iface

class InformationRetriever(object):
    def __init__(self):
        pass
    
    def retrieve(self, iface, point1, point2):
        if point1.x() < point2.x():
            self.left = point1.x()
            self.right = point2.x()
        else:
            self.left = point2.x()
            self.right = point1.x()
            
        if point1.y() < point2.y():
            self.top = point1.y()
            self.bottom = point2.y()
        else:
            self.top = point2.y()
            self.bottom = point1.y()
        
        self.layer = iface.activeLayer()
        dataProvider = self.layer.dataProvider()
        
        extent = dataProvider.extent()
        width = dataProvider.xSize() if dataProvider.capabilities() & dataProvider.Size else 1000
        height = dataProvider.ySize() if dataProvider.capabilities() & dataProvider.Size else 1000
        
        xRes = extent.width() / width
        yRes = extent.height() / height
    
        point = iface.mapCanvas().getCoordinateTransform().toMapCoordinates(self.left, self.top)
        self.absoluteLeft = int(floor((point.x() - extent.xMinimum()) / xRes))
        self.absoluteTop = int(floor((extent.yMaximum() - point.y()) / yRes))
        point = iface.mapCanvas().getCoordinateTransform().toMapCoordinates(self.right, self.bottom)
        self.absoluteRight = int(floor((point.x() - extent.xMinimum()) / xRes))
        self.absoluteBottom = int(floor((extent.yMaximum() - point.y()) / yRes))
        
        self.dataSource = dataProvider.dataSourceUri()
        self.crs = self.layer.crs()
    
    def setCoordinates(self, coord1, coord2):
        self.coord1 = coord1
        self.coord2 = coord2
        
    def getCoordinates(self):
        return self.coord1, self.coord2
    
    def getSelection(self):
        return self.top, self.left, self.bottom, self.right
    
    def getAbsoluteSelection(self):
        return self.absoluteTop, self.absoluteLeft, self.absoluteBottom, self.absoluteRight
        
    def getDataSource(self):
        return self.dataSource
    
    def getLayer(self):
        return self.layer
    
    def getCRS(self):
        return self.crs