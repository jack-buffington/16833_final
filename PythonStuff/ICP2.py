import numpy as np
from convertScanToXY import convertScanToXY
from scipy.spatial.distance import pdist,cdist
import operator
import pdb
import math
import time

def distance(x1,y1,x2,y2):
    dist=math.sqrt(((float(x1)-float(x2))*(float(x1)-float(x2)))+((float(y1)-float(y2))*(float(y1)-float(y2))))
    return dist



def closestPoints(old,new):
    distances = cdist(old,new,'euclidean')
    # distances is a matrix where rows correspond to points in the 'old' matrix and 
    # cols correspond to points in the 'new' matrix.
    indices = np.argmin(distances, axis = 0)
    closest = old[indices] # gives me 
    return closest




def doOneIteration(XY1,XY2):

#   Find the closest point in XY2 for each point in XY1
    closestPts=closestPoints(XY1,XY2)

#   Find the covariance between the 2 matrices
    cov=np.matmul((np.transpose(XY2)),closestPts)
    #pdb.set_trace()
    
#   Use that to find the rotation
    U, s, V = np.linalg.svd(cov, full_matrices=True)
    rotationMatrix = np.matmul(V,U.T)

#   Find the optimal translation
    XY2 = np.matmul(rotationMatrix,XY2.T).T

#   Find their average translation from their corresponding closest points
    diffs=XY2-closestPts
    offset=np.mean(diffs,axis=0)
    translation=-offset
    
#   Calculate the error in alignment as the sum of squared distances between point matches
    err=math.sqrt((offset[0])*(offset[0])+(offset[1])*(offset[1]))

    return rotationMatrix, translation, err



def ICP2(XY1, XY2):
	# Convert from polar to cartesian coordinates
    # XY1 = convertScanToXY(XY1)
    # XY2 = convertScanToXY(XY2)
    start_time = time.time()

    #########################################
    # Interpolate the first scan as necessary
    #########################################
    # This is approximating point to plane ICP but instead of projecting onto the 
    # normal, I am just creating more points in areas where things are sparse. 
    numberOfPoints = XY1.shape[0]
    C = np.zeros([2,2]) 
    #maxDist = .07
    maxDist = 50

    for I in range(numberOfPoints - 2): 
        A = XY1[I,:]
        B = XY1[I+1,:] 
        C[0,:] = A           # and is used to find the distance betwen them
        C[1,:] = B
        distance = pdist(C)

        if distance > maxDist:
            XY1 = interpolatePoints(A,B, distance, maxDist, XY1)


    # Check the first and last points as a special case
    A = XY1[numberOfPoints-1,:]
    B = XY1[0,:]
    C[0,:] = A
    C[1,:] = B

    distance = pdist(C)
    if distance > maxDist:
        XY1 = interpolatePoints(A,B, distance, maxDist, XY1)

    elapsed_time = time.time() - start_time



    ######################################
    # Iterate the closest points algorithm
    ######################################
    totalTranslation = np.matrix('0 0')
    totalRotationMatrix = np.matrix('1 0; 0 1');
    maxIterations = 30; # takes about .043 seconds per iteration
    errorThreshold = .00001;

    for I in range (1,maxIterations):
        rotationMatrix, translation, err = doOneIteration(XY1,XY2)

        if err < errorThreshold:
            break

        XY2 = np.transpose(np.matmul(rotationMatrix,np.transpose(XY2)))
        XY2 = XY2 + translation

        totalTranslation = np.transpose(np.matmul(rotationMatrix,np.transpose(totalTranslation))) + translation
        totalRotationMatrix = np.matmul(rotationMatrix,totalRotationMatrix)

    rotationMatrix = totalRotationMatrix;
    translation = totalTranslation;
    
    elapsed_time = time.time() - start_time
    print 'Time to do ICP: ', elapsed_time

    return [translation,rotationMatrix]





def interpolatePoints(A,B, distance, maxDistance, pointArray):
    numberOfInterpolatedPoints = int(distance / maxDistance)
    offset = (B - A)/float(numberOfInterpolatedPoints + 1)
    currentLocation = A
    for J in range(numberOfInterpolatedPoints):
        currentLocation += offset
        pointArray = np.append(pointArray,[currentLocation], axis = 0)
    return pointArray




