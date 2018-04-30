from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
from ICP09 import * 
import time
import numpy as np
import pdb



fileData = loadData('firstFloor.txt')
resolution = 10;
insertionDistance = 250
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

occupancyMap = insertPoints(lastXY/resolution, occupancyMap)

robotPos = np.array([[0,0,0]])
visualizeMap(occupancyMap,robotPos)

cumulativeTransform = np.eye(3)
lastTransform = np.eye(3)

C = np.zeros([2,2])  # this is necessary in Python to use pdist

count = 1
for i in range(firstFrame,lastFrame,10): 

    print i 
    XY = convertScanToXY(fileData[i])

    # Strip away any 'points' that ended up being [0 0]
    temp = XY == 0 # This will be true and false
    temp = temp * np.ones(temp.shape) # should now be 0's and 1's
    temp = np.sum(temp, axis = 1) < 2 # should be true and false correspoinding
                                      # to rows that we want to keep (True)
    XY = XY[temp] # should be just coordinates that aren't [0 0]

    currentRobotPos = robotPos[len(robotPos)-1];
    lastXY = getPointsWithinRadius(occupancyMap,currentRobotPos, 5000, cumulativeTransform);

    
    visualizeScan(lastXY, 1,'b');
    visualizeScan(XY, 0, 'r');
    #pdb.set_trace()
    
    #thisTransform = ICP07( XY, lastXY , lastTransform)
    thisTransform = ICP09(lastXY, XY , lastTransform)

    lastTransform = thisTransform;
    
    cumulativeTransform = np.matmul(cumulativeTransform,thisTransform);
    print 'cumulative transform ', cumulativeTransform
    # Plot the transformed points
    XY = np.append(XY,np.ones([len(XY),1]), axis=1)
    XY = np.matmul( XY, cumulativeTransform.T)

    occupancyMap = insertPoints(XY/resolution, occupancyMap)

    thisRobotPos = np.matmul(cumulativeTransform, np.array([0,0,1]))
    
    # Update the robot pose
    robotAngle = math.atan2(cumulativeTransform[1,0], cumulativeTransform[0,0])
    robotPos = np.append(robotPos, [[thisRobotPos[0]/resolution, thisRobotPos[1]/resolution, robotAngle]], axis=0) 
    
    visualizeMap(occupancyMap, robotPos)

