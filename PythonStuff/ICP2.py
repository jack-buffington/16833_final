import numpy as np
from convertScanToXY import convertScanToXY
from scipy.spatial.distance import pdist,cdist
import operator
import pdb
import math

def distance(x1,y1,x2,y2):
    dist=math.sqrt(((float(x1)-float(x2))*(float(x1)-float(x2)))+((float(y1)-float(y2))*(float(y1)-float(y2))))
    return dist

def ClosestPoints(old,new):
    
    closest=[]
    for i in range(len(new)):
        index=0
        min_dist=238900
        for j in range(len(old)):
            dist=distance(new[i][0],new[i][1],old[j][0],old[j][1])
            if dist<min_dist:
                min_dist=dist
                index=j
        closest.append([old[index][0],old[index][1]])

    return np.array(closest)


def doOneIteration(XY1,XY2):

#   Find the closest point in XY2 for each point in XY1

    closestPoints=ClosestPoints(XY1,XY2)
    # print 'ClosestPoints:', closestPoints[1:10,:]
    # print 'XY2', XY2[1:10,:]
    
#     distances=cdist(XY1,XY2)
#     print 'distances', distances
    # pdb.set_trace()
# #   distances is a matrix where each row corresponds to a point in XY1
# #   and each column corresponds to a point in XY2
# #   The values are the distances between those points
#     index,value=min(enumerate(distances,1,key=operator.itemgetter(1)))
   
    
#   Create a new matrix that contains the nearest point to each point in centeredXY2
    # closestPoints = XY1[index,:]
    
#   Find the covariance between the 2 matrices
    cov=np.matmul((np.transpose(XY2)),closestPoints)
    pdb.set_trace()
    
#   Use that to find the rotation
    U, s, V = np.linalg.svd(cov, full_matrices=True)
    rotationMatrix=V*np.transpose(U)
    
#   Find the optimal translation
#   Rotate the points
    XY2=np.transpose(np.matmul(rotationMatrix,(np.transpose(XY2))))
    
#   Find their average translation from their corresponding closest points
    diffs=XY2-closestPoints
    offset=np.mean(diffs,axis=0)
    translation=-offset
    
#   Calculate the error in alignment as the sum of squared distances between point matches
    err=math.sqrt((offset[0])*(offset[0])+(offset[1])*(offset[1]))
    # pdb.set_trace()
    return rotationMatrix, translation,err

def ICP2(XY1, XY2):
	# Convert from polar to cartesian coordinates
    # XY1 = convertScanToXY(XY1)
    # XY2 = convertScanToXY(XY2)

    #########################################
    # Interpolate the first scan as necessary
    #########################################
    numberOfPoints = XY1.shape[0]

    maxDist = .07
    
    for I in range(numberOfPoints -2):
    	A = XY1[I,:]
    	B = XY1[I+1,:]
    	print 'A''s type: ', type(A)
    	#C = np.concatenate((A, B), axis=0)
    	#C=np.array(A.append(B))
    	#C = np.matrix(A;B)
    	C = np.zeros([2,2])
    	C[0,:] = A
    	C[1,:] = B

    	print 'A: ', A
    	print 'B: ', B

    	print 'C: ', C
    	distance = pdist(C)
    	if distance > maxDist:
    		numberOfInterpolatedPoints = int(distance / maxDist)
    		offset = (B - A)/float(numberOfInterpolatedPoints + 1)

    		currentLocation = A
    		for J in range(numberOfInterpolatedPoints):
    			currentLocation += offset
    			# print 'Shape of XY1: ', XY1.shape 
    			# print 'Shape of currentLocation: ', currentLocation.shape
    			# print 'currentLocation: ', np.transpose(currentLocation)
    			# print 'XY1''s type: ' , type(XY1)
    			# print 'currentLocation''s type: ', type(currentLocation)

    			# print XY1
    			# XY1 = np.concatenate((XY1,np.transpose(currentLocation)), axis = 0)
    			np.append(XY1,np.array([currentLocation]), axis = 0)
    # Check the first and last points as a special case
	A = XY1[numberOfPoints-1,:]
	B = XY1[0,:]
   	C[0,:] = A
   	C[1,:] = B

	distance = pdist(C)
	if distance > maxDist:
		numberOfInterpolatedPoints = int(distance / maxDist)
		offset = (B - A)/float(numberOfInterpolatedPoints + 1)

		currentLocation = A
		for J in range(numberOfInterpolatedPoints):
			currentLocation += offset
			np.append(XY1,np.array([currentLocation]), axis = 0)


    ######################################
    # Iterate the closest points algorithm
    ######################################
	totalTranslation = np.matrix('0 0')
	totalRotationMatrix = np.matrix('1 0; 0 1');
	maxIterations = 50;
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

	return [rotationMatrix, translation]







