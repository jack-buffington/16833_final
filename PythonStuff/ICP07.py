import numpy as np
from convertScanToXY import convertScanToXY
from scipy.spatial.distance import pdist,cdist
import operator
import pdb
import math
import time

# def distance(x1,y1,x2,y2):
#     dist=math.sqrt(((float(x1)-float(x2))*(float(x1)-float(x2)))+((float(y1)-float(y2))*(float(y1)-float(y2))))
#     return dist



def closestPoints(old,new):
    distances = cdist(old,new,'euclidean')
    # distances is a matrix where rows correspond to points in the 'old' matrix and 
    # cols correspond to points in the 'new' matrix.
    indices = np.argmin(distances, axis = 0)
    closest = old[indices] 
    return closest







def doOneIteration(XY1,XY2):
#   Find the closest point in XY2 for each point in XY1
    closestPts=closestPoints(XY1,XY2)

    #pdb.set_trace()
    
#   Find the covariance between the 2 matrices
    cov=np.matmul((np.transpose(XY2)),closestPts)
    
    
#   Use that to find the rotation
    U, s, V = np.linalg.svd(cov, full_matrices=True)
    rotationMatrix = np.matmul(V,U.T)

#   Find the optimal translation
    XY2 = np.matmul(XY2, rotationMatrix.T)

#   Find their average translation from their corresponding closest points
    diffs=XY2-closestPts
    offset=np.mean(diffs,axis=0)
    translation=-offset
    
#   Calculate the error in alignment as the sum of squared distances between point matches   
    err=math.sqrt((offset[0])*(offset[0])+(offset[1])*(offset[1]))



    return rotationMatrix, translation, err







def ICP07(XY1, XY2, transformationSeed):



    #start_time = time.time()

    #########################################
    # Interpolate the first scan as necessary
    #########################################
    # This is approximating point to plane ICP but instead of projecting onto the 
    # normal, I am just creating more points in areas where things are sparse. 
    numberOfPoints = XY1.shape[0]
    C = np.zeros([2,2])  # this is necessary in Python to use pdist

    maxDist = 50

    

    for I in range(numberOfPoints - 1): 
        A = XY1[I,:]
        B = XY1[I+1,:] 

        C[0,:] = A           # and is used to find the distance betwen them
        C[1,:] = B
        distance = pdist(C)

        
        #print 'distance: ', distance
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

    #elapsed_time = time.time() - start_time





    # print 'Stop point just before ICP'
    # pdb.set_trace()
    # ###############
    # Do the ICP part
    # ###############

    translation, rotationMatrix = actualICP(XY1, XY2, transformationSeed)

    # rotate and translate the XY2 points
    XY2temp = np.matmul(XY2,rotationMatrix.T)  # Resulting in a 154x1 matrix
    XY2temp = XY2temp + translation;


    # #########################################
    # Remove points that don't align very well:
    # #########################################


    # * Find the distances to all of the closest points 
    tempPoints = closestPoints(XY1,XY2temp)
    minDistances = np.linalg.norm(XY2temp - tempPoints,axis = 1)

    # * Figure out if there are any points that don't sit close to any points in the old
    #     To find points that are outliers, look for points that are more than 1.5 times
    #     the maxDist 

    pointsToKeep = minDistances < maxDist * 1.5; # True and False in Python
    count = np.array(range(len(pointsToKeep)))
    pointsToKeep = pointsToKeep * count
    pointsToKeep = pointsToKeep[pointsToKeep > 0] 

    # and temporarily remove them from the new set.
    XY2refined = XY2[pointsToKeep]





    # ##############################################################
    # Do ICP again with the two sets of points that match up better.
    # ##############################################################

    trans, rot = actualICP(XY1, XY2refined, transformationSeed)


    
    # transformMatrix = np.matrix([[rot[0,0], rot[0,1], trans[0]],
    #                              [rot[1,0], rot[1,1], trans[1]],
    #                              [0,               0,         1]]);

    transformMatrix = np.array([[rot[0,0], rot[0,1], trans[0]],
                                 [rot[1,0], rot[1,1], trans[1]],
                                 [0,               0,         1]]);

    return transformMatrix







def interpolatePoints(A,B, distance, maxDistance, pointArray):

    # print pointArray
    # pdb.set_trace()
    
    numberOfInterpolatedPoints = int(math.floor(distance / maxDistance))
    
    offset = (B - A)/float(numberOfInterpolatedPoints + 1)

    #currentLocation = A
    currentLocation = np.array([A[0], A[1]])
    
    for J in range(numberOfInterpolatedPoints):
        currentLocation += offset 
        pointArray = np.append(pointArray,[currentLocation], axis = 0)
    return pointArray


# def interpolatePoints2(A,B, distance, maxDistance, pointArray):
#     numberOfInterpolatedPoints = int(math.floor(distance / maxDistance))
#     startX = A[0]
#     endX = B[0]
#     startY = A[1]
#     endY = B[1]

#     Xs = np.linspace(startX,endX,numberOfInterpolatedPoints + 2)
#     Ys = np.linspace(startY,endY,numberOfInterpolatedPoints + 2)
    
#     # Concatenate the two 
#     XYs = np.array([Xs,Ys]).T

#     # Cut off the first and last values
#     XYs = XYs[1:XYs.shape[0] - 1]
#     pointArray = 






def actualICP(XY1, XY2, transformationSeed):
    #totalTranslation = np.matrix('0 0')
    totalRotationMatrix = np.matrix('1 0; 0 1');
    maxIterations = 50; 
    errorThreshold = .00001;

    # Break the transformation seed up into rotation and translation matrices.
    rotSeed = transformationSeed[0:2,0:2]
    transSeed = transformationSeed[0:2,2].T

    # set up the initial transformation
    XY2 = np.matmul(XY2, rotSeed.T)
    XY2 = XY2 + transSeed

    # print 'Stopping in actualICP'
    # pdb.set_trace()
    totalRotationMatrix = rotSeed;
    totalTranslation = transSeed;


    for I in range (1,maxIterations):

        rotationMatrix, translation, err = doOneIteration(XY1,XY2)
        if err < errorThreshold:
            break

        XY2 = np.matmul(XY2,rotationMatrix.T)
        XY2 = XY2 + translation

        totalTranslation = np.matmul(totalTranslation,rotationMatrix.T) + translation 
        totalRotationMatrix = np.matmul(rotationMatrix,totalRotationMatrix)

    rotationMatrix = totalRotationMatrix;
    translation = totalTranslation;

    return [translation,rotationMatrix]
