'''
Created on Sep 28, 2018

@author: Seokyong Hong
'''

class PBTXTWriter(object):
    def __init__(self):
        self.file = None
    
    def open(self, path):
        self.file = open(path, "w")
    
    def write(self, id, label):
        if self.file is not None:
            self.file.write('item {\n')
            self.file.write('\tid: ' + str(id) + '\n')
            self.file.write('\tname: \'' + label + '\'\n')
            self.file.write('}\n')
    
    def close(self):
        if self.file is not None:
            self.file.close()