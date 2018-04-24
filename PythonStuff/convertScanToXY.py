import numpy as np
import math
# Converts the points from polar coortinates to cartesian.  

def convertScanToXY(scan):
    # scans are in rows that are [angle range]  Angles are in degrees
    numberOfPoints = scan.shape[0]   

    returnMatrix = np.zeros(scan.shape)
    for I in range(numberOfPoints):
        angle = (scan[I][0] * np.pi) / 180 # Convert the angle from degrees to radians

        returnMatrix[I][0] = scan[I][1] * math.cos(angle)/10.0 # X = distance * cos(angle)
        returnMatrix[I][1] = scan[I][1] * math.sin(angle)/10.0 # Y = distance * sin(angle)

    return returnMatrix
 
            
