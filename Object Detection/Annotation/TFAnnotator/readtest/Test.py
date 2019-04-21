'''
Created on Sep 3, 2018

@author: Seokyong Hong
'''
import numpy
import tensorflow as tflow
import matplotlib.pyplot as plot

if __name__ == '__main__':
    images = []
    iterator = tflow.python_io.tf_record_iterator(path = "/home/phantom/Desktop/test.tfrecord")
    
    for stringRecord in iterator:
        example = tflow.train.Example()
        example.ParseFromString(stringRecord)
        
        width = int(example.features.feature['image/width'].int64_list.value[0])
        height = int(example.features.feature['image/height'].int64_list.value[0])
        label = int(example.features.feature['image/class/label'].int64_list.value[0])
        image = (example.features.feature['image/encoded'].bytes_list.value[0])
        
        image = numpy.fromstring(image, dtype = numpy.uint8)
        image = image.reshape((height, width, -1))
        
        print("Width: " + str(width))
        print("Height: " + str(height))
        print("Label: " + str(label))
        
        plot.imshow(image)
        plot.show()