'''
Created on Sep 2, 2018

@author: Seokyong Hong
'''
import tensorflow as tflow

def _int64_feature(value):
    return tflow.train.Feature(int64_list = tflow.train.Int64List(value = [value]))

def _bytes_feature(value):
    return tflow.train.Feature(bytes_list = tflow.train.BytesList(value = [value]))

def _bytes_list_feature(value):
    return tflow.train.Feature(bytes_list = tflow.train.BytesList(value = value))

def _int64_list_feature(value):
    return tflow.train.Feature(int64_list = tflow.train.Int64List(value = value))

def _float_list_feature(value):
    return tflow.train.Feature(float_list = tflow.train.FloatList(value = value))