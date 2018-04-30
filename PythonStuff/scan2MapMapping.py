from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
from ICP08 import * 
import time
import numpy as np
import pdb



fileData = loadData('firstFloor.txt')

insertionDistance = 500
visualizationDivider = 5; # only show every 5th frame.

firstFrame = 90 - 1
lastFrame = len(fileData) - 1

occupancyMap = initMap()
lastXY =  convertScanToXY(fileData[firstFrame - 5])

# Strip away any 'points' that ended up being [0 0]
temp = lastXY == 0 # This will be true and false
temp = temp * np.ones(temp.shape) # should now be 0's and 1's
temp = np.sum(temp, axis = 1) < 2 # should be true and false correspoinding
                                  # to rows that we want to keep (True)

occupancyMap = insertPoints(lastXY/10, occupancyMap)
lastInsertionPosition = np.array([0,0]) 
lastInsertionAngle = 0; # radians


robotPos = np.array([[0,0,0]])
visualizeMap(occupancyMap,robotPos)

# cumulativeTransform = np.matrix([[1,0,0],
#                                  [0,1,0],
#                                  [0,0,1]]) 
cumulativeTransform = np.eye(3)
lastTransform = np.eye(3)

C = np.zeros([2,2])  # this is necessary in Python to use pdist

count = 1
for i in range(firstFrame,lastFrame,1): 

    print '-----------------------------'
    print '-----------------------------'
    print i 
    XY = convertScanToXY(fileData[i])


    # Strip away any 'points' that ended up being [0 0]
    temp = XY == 0 # This will be true and false
    temp = temp * np.ones(temp.shape) # should now be 0's and 1's
    temp = np.sum(temp, axis = 1) < 2 # should be true and false correspoinding
                                      # to rows that we want to keep (True)
    XY = XY[temp] # should be just coordinates that aren't [0 0]

    currentRobotPos = robotPos[len(robotPos)-1];
    print 'size of occupancy map: ', occupancyMap.shape
    lastXY = getPointsWithinRadius(occupancyMap,currentRobotPos, 1200);#get the points from the model around a radius of 500 cm from current robot position
    #****use this to visualize the model scan and the input scan 
    visualizeScan(lastXY, 1,'b');
    visualizeScan(XY, 0, 'r');
    #pdb.set_trace()
    
    #thisTransform = ICP07( XY, lastXY , lastTransform)
    thisTransform = ICP08(lastXY, XY , lastTransform)

    print 'thisTransform'
    print thisTransform
    lastTransform = thisTransform;

    cumulativeTransform = np.matmul(cumulativeTransform,thisTransform);
    
    # Plot the transformed points
    XY = np.append(XY,np.ones([len(XY),1]), axis=1)
    XY = np.matmul( XY, cumulativeTransform.T)


    # Figure out what the current pose is and determine if it should insert the points or not
    # OPTION 1:  JUST SPACE OUT HOW FAR IT CAN GO BEFORE POINTS ARE ADDED IN.
    # OPTION 2:  KEEP TRACK OF WHERE POINTS WERE ADDED IN AND ONLY PUT THEM IN IF IT IS FARTHER THAN 
    #          SOME PREDETERMINED DISTANCE
    # OPTION 3: ONLY ADD IN POINTS THAT DON'T HAVE ANOTHER POINT ALREADY IN THE MAP THAT IS CLOSE TO THEM

    thisPosition = np.array([cumulativeTransform[0,2], cumulativeTransform[1,2]])
    thisAngle = math.atan2(cumulativeTransform[1,0], cumulativeTransform[0,0])

    # Find the distance between this pose and the last one inserted
    #delta = thisPosition - lastInsertionPosition
    C[0,:] = thisPosition           # and is used to find the distance betwen them
    C[1,:] = lastInsertionPosition
    distance = pdist(C)
    print 'distance: ', distance

    if distance > insertionDistance:
        occupancyMap = insertPoints(XY/10, occupancyMap)
        lastInsertionPosition = thisPosition
        lastInsertionAngle = thisAngle

    thisRobotPos = np.matmul(cumulativeTransform, np.array([0,0,1]))
    
    # Update the robot pose
    robotAngle = math.atan2(cumulativeTransform[1,0], cumulativeTransform[0,0])
    robotPos = np.append(robotPos, [[thisRobotPos[0]/10, thisRobotPos[1]/10, robotAngle]], axis=0) 
    
    count = count + 1
    if count % visualizationDivider == 0:
        visualizeMap(occupancyMap, robotPos)

pdb.set_trace()  # make it pause so we can see the entire map.