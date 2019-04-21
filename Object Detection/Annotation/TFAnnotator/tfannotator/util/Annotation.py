'''
Created on Sep 2, 2018

@author: Seokyong Hong
'''
class Annotation(object):
    def __init__(self, path, top, left, bottom, right, index, label):
        self.path = path
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.index = index
        self.label = label
