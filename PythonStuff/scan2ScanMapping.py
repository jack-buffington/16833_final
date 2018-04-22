from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
from ICP2 import * 
import time
import numpy as np
import pdb

data = loadData('firstFloor.txt')
occupancyMap = initMap();
prevScan =  convertScanToXY(data[0]);
occupancyMap = insertPoints(prevScan, occupancyMap);
robotPos = np.array([0,0]);
visualizeMap(occupancyMap,robotPos );
globalTrans = np.array([0,0]);
globalRot = np.array([[1,0],[0,1]]); 

for i in range(1,100):
    newScan = convertScanToXY(data[i]);
    trans, rot = ICP2(prevScan, newScan);
    globalRot = np.matmul(rot, globalRot); 
    globalTrans = globalTrans + trans; #maybe need to rotate the translation
    newScanTranslated = newScan + trans;
    newScanTranslatedAndRotated = np.matmul(newScanTranslated, rot);
    
    occupancyMap = insertPoints(newScanTranslatedAndRotated, occupancyMap);
    robotPos = np.matmul( (robotPos + trans),rot);
    robotPos = np.array([robotPos[0,0], robotPos[0,1]]); 
    visualizeMap(occupancyMap, robotPos);
    time.sleep(0.1);
    

'''for i in data:
    scan = convertScanToXY(i);
    occupancyMap = insertPoints(scan, occupancyMap);
    visualizeMap(occupancyMap, np.array([0,0])); 
    time.sleep(0.1);'''
