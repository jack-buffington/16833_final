import numpy as np
from convertScanToXY import convertScanToXY
from SVD import find_rotation
from CentroidandClosestPoints import findCentroid, ClosestPoints



def ICP(oldScanPolar, newScanPolar):
    print 'old scan polar: '
    print type(oldScanPolar) 

    # Convert from polar to cartesian coordinates
    oldScanXY = convertScanToXY(oldScanPolar)
    newScanXY = convertScanToXY(newScanPolar)

    print 'old scan cartesian: '
    print type(oldScanXY) 

    # Find the centroids
    oldCentroid = findCentroid(oldScanXY)
    newCentroid = findCentroid(newScanXY)

    print 'old scan Centroid: '
    print type(oldCentroid) 

    # Remove the centroids
    oldScanXYcentered = oldScanXY - oldCentroid
    newScanXYcentered = newScanXY - newCentroid

    print 'old scan Centered: '
    print type(oldScanXYcentered) 

    print 'shape of old scan: ', oldScanXYcentered.shape
    print 'shape of new scan: ', newScanXYcentered.shape
   


    # Find the closest points by Euclidean distance
    pointMatches = ClosestPoints(oldScanXYcentered, newScanXYcentered)
    #print'matches:', pointMatches
    # find the covariance between the new scan and the point matches and then find the rotation 
    rotMatrix = find_rotation(pointMatches, newScanXYcentered)

    # Find the translation.  
    translation = np.transpose(np.matrix(oldCentroid)) - rotMatrix * np.transpose(np.matrix(newCentroid))


    return translation,rotMatrix

