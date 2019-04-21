'''
Created on Sep 1, 2018

@author: Seokyong Hong
'''
import io
import numpy
from PIL import Image
from osgeo import gdal

class ImageLoader(object):
    def __init__(self, path):
        self.dataset = gdal.Open(path, gdal.GA_ReadOnly)
        self.width = self.dataset.RasterXSize
        self.height = self.dataset.RasterYSize
        self.depth = self.dataset.RasterCount
    
    def load(self):
        if self.depth != 3:
            return None
        
        xOffset = 0
        yOffset = 0
        cropWidth = self.width
        cropHeight = self.height
        bands = (numpy.array(self.dataset.GetRasterBand(band).ReadAsArray(xoff = xOffset, yoff = yOffset, win_xsize = cropWidth, win_ysize = cropHeight, buf_xsize = cropWidth, buf_ysize = cropHeight, buf_type = gdal.GDT_Byte)) for band in range(1, self.depth + 1))
        bands = numpy.dstack(bands)
        
        return self.convert2Jpeg(bands), cropWidth, cropHeight
    
    def convert2Jpeg(self, bands):
        with io.BytesIO() as stream:
            image = Image.fromarray(bands)
            image.save(stream, format = 'JPEG')
            return stream.getvalue()