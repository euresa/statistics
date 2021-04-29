# Adapted from: Ujaval Gandhi, 2014
#Modified by Samuel Eure, 2018
#This code will (1) find features which are touching or overlapping with one another,
#               (2) call these features neighbors, and add them into the shapefile.
#               (3) Neighbors will be added in the form of a comma-separated list
#Run code from QGIS python console
#Have the shapefile of interst selected

#******   Parameters   ******************
_NAME_FIELD = 'fid'
_NEW_NEIGHBORS_FIELD = 'NEIGHBORS'
#****************************************


from qgis.utils import iface
from PyQt4.QtCore import QVariant

PLayerName = ' precinct2010 Polygon'
VLayerName = ' 2010_vtds_merged Polygon'


layers = qgis.utils.iface.legendInterface().layers()

for layerQ in layers:
    print layerQ.name()
    if layerQ.name() == PLayerName:
        layer=layerQ
    elif layerQ.name() == VLayerName:
        vLayer = layerQ


layer.startEditing()
layer.dataProvider().addAttributes(
        [QgsField(_NEW_NEIGHBORS_FIELD, QVariant.String)])
layer.updateFields()
feature_dict = {f.id(): f for f in layer.getFeatures()}
index = QgsSpatialIndex()
for f in feature_dict.values():
    index.insertFeature(f)
# Loop through all features and find features that touch each feature
for f in feature_dict.values():
    print 'Working on %s' % f[_NAME_FIELD]
    geom = f.geometry()
    # Find all features that intersect the bounding box of the current feature.
    # We use spatial index to find the features intersecting the bounding box
    # of the current feature. This will narrow down the features that we need
    # to check neighboring features.
    intersecting_ids = index.intersects(geom.boundingBox())
    # Initalize neighbors list and sum
    neighbors = []
    neighbors_sum = 0
    for intersecting_id in intersecting_ids:
        # Look up the feature from the dictionary
        intersecting_f = feature_dict[intersecting_id]
        # For our purpose we consider a feature as 'neighbor' if it touches or
        # intersects a feature. We use the 'disjoint' predicate to satisfy
        # these conditions. So if a feature is not disjoint, it is a neighbor.
        if (f != intersecting_f and
            not intersecting_f.geometry().disjoint(geom)):
            neighbors.append(str(intersecting_f[_NAME_FIELD]))
    f[_NEW_NEIGHBORS_FIELD] = ','.join(neighbors)
    layer.updateFeature(f)
layer.commitChanges()
print 'Processing complete.'