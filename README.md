# TDAT
<h3>Data Annotation Tool for Tensorflow Analysis (TDAT)</h3>

### Description
Tnesorflow object detection requires annotated datasets represented in RFRecord format. Existing tools such as [labelImg](https://github.com/tzutalin/labelImg) and [VoTT](https://github.com/Microsoft/VoTT) support data annotation but they do not support satellite images in GeoTIFF, which is one of frequently used raster data formats in geo-analysis. TDAT supports object annotation, being plugged into [QGIS](https://qgis.org/ko/site/), a popular GIS application.
<p align="center">
  <image width="70%" src="https://github.com/fender3kr/Images/blob/master/TDAT/TDAT.png">
</p>

### Requirements
* Ubuntu Linux
* Python 3.6
* QGIS 3.2 Bonn
* Tensorflow

### Installation
* Download the project
* Copy <PROJECT_ROOT>/ObjectDetection/Annotation/TFAnnotator/tfannotator to ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
* Launch QGIS 3.2
* Menu -> Plugins -> Manage and Install Plugins ... -> All -> check "Tensorflow Dataset Annotation Tool"

### How to use
* Open a GeoTIFF raster
* Load the TDAT plugin by clicking the first button in the toolbar:
![](https://github.com/fender3kr/Images/blob/master/TDAT/Load.png)

* Add labels: write a label in the ComboBox in "Labels" group and press "Add Label"
* Delete labels: select a label in the ComboBox in "Labels" group and press "Delete Label"
![](https://github.com/fender3kr/Images/blob/master/TDAT/Label.png)

* For the tool to work, loaded raster images must be displayed in the same coordinate reference system (CRS) as of those images. That is, canvas CRS must be set with the CRS of image. The tool automatically does this by clicking the third button in the toolbar:
![](https://github.com/fender3kr/Images/blob/master/TDAT/Fit.png)

* To select an object, click the second button in the toolbar:
![](https://github.com/fender3kr/Images/blob/master/TDAT/Select.png)

* Then, draw a rectangle on the desired object in the canvas, select a label to give, and click "Add Annotation" button:
![](https://github.com/fender3kr/Images/blob/master/TDAT/AddAnnotation.png)
* To remove an annotation, select a target annotation in the table in "Annotations" group and click "Delete Annotation" button.
* After annotating all objects, you can export the annotations to a TFRecord file by clicking "Export" button in "Clear/Export" group. Clicking "Clear All" button removes all annotations.

### How to participate
This tool was developed with 
* [Eclipse Photon](http://www.eclipse.org/)
* [PyDev (Eclipse Plugin for Python)](http://www.pydev.org/) 
* [PyQT5](https://pypi.org/project/PyQt5/)
