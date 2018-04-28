from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
from ICP07 import * 
import time
import numpy as np
import pdb



fileData = loadData('firstFloor.txt')

firstFrame = 90 - 1
lastFrame = len(fileData) - 1

occupancyMap = initMap()

lastXY =  convertScanToXY(fileData[firstFrame - 5])

# Strip away any 'points' that ended up being [0 0]
temp = lastXY == 0 # This will be true and false
temp = temp * np.ones(temp.shape) # should now be 0's and 1's
temp = np.sum(temp, axis = 1) < 2 # should be true and false correspoinding
                                  # to rows that we want to keep (True)
lastXY = lastXY[temp] # should be just coordinates that aren't [0 0]

occupancyMap = insertPoints(lastXY/10, occupancyMap)

robotPos = np.array([[0,0]])
visualizeMap(occupancyMap,robotPos)

# cumulativeTransform = np.matrix([[1,0,0],
#                                  [0,1,0],
#                                  [0,0,1]]) 
cumulativeTransform = np.eye(3)
lastTransform = np.eye(3)


for i in range(firstFrame,lastFrame,5): 
    XY = convertScanToXY(fileData[i])


    # Strip away any 'points' that ended up being [0 0]
    temp = XY == 0 # This will be true and false
    temp = temp * np.ones(temp.shape) # should now be 0's and 1's
    temp = np.sum(temp, axis = 1) < 2 # should be true and false correspoinding
                                      # to rows that we want to keep (True)
    XY = XY[temp] # should be just coordinates that aren't [0 0]


    thisTransform = ICP07(lastXY, XY, lastTransform)
    lastTransform = thisTransform
    #pdb.set_trace();
    lastXY = XY

    cumulativeTransform = np.matmul(cumulativeTransform,thisTransform);
    
    # Plot the transformed points
    XY = np.append(XY,np.ones([len(XY),1]), axis=1)
    XY = np.matmul( XY, cumulativeTransform.T)


    occupancyMap = insertPoints(XY/10, occupancyMap)
    thisRobotPos = np.matmul(cumulativeTransform, np.array([0,0,1]))
    
    # Update the robot pose
    robotPos = np.append(robotPos, [[thisRobotPos[0]/10, thisRobotPos[1]/10]], axis=0); 
    visualizeMap(occupancyMap, robotPos)
    #time.sleep(0.1)
    
    


