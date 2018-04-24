from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
from ICP2 import * 
import time
import numpy as np
import pdb

data = loadData('firstFloor.txt')
#data = loadData('scanData.txt')
occupancyMap = initMap();
prevScan =  convertScanToXY(data[0]);
occupancyMap = insertPoints(prevScan, occupancyMap);
robotPos = np.array([0,0]);
visualizeMap(occupancyMap,robotPos );
#globalTrans = np.matrix([[0,0]]);
#globalRot = np.matrix([[1,0],[0,1]]);
globalTransform = np.matrix([[1,0,0],
                             [0,1,0],
                             [0,0,1]]); 
#pdb.set_trace();

for i in range(80,200):
    newScan = convertScanToXY(data[i]);
    trans, rot = ICP2(prevScan, newScan);
    intermediateTransform = np.matrix([ [rot[0,0], rot[0,1],trans[0,0]],
                                        [rot[1,0], rot[1,1], trans[0,1]],
                                        [0,0,1]]);
    globalTransform = np.matmul(globalTransform,intermediateTransform);
    
    #globalTrans = globalTrans + (np.matmul(globalRot,trans.T)).T;
    #globalRot = np.matmul(globalRot,rot);
    updatedScan = np.append(newScan,np.ones([len(newScan),1]), axis=1);
    #updatedScan = (np.matmul( globalRot,newScan.T)).T;
    #updatedScan = updatedScan + globalTrans;
    updatedScan = np.matmul( updatedScan, globalTransform.T); 
    
    occupancyMap = insertPoints(updatedScan, occupancyMap);
    robotPos = np.array([0,0]);
    #robotPos = (np.matmul(globalRot, robotPos.T)).T;
    #robotPos = globalTrans + robotPos; 
    #robotPos = np.array([robotPos[0,0], robotPos[0,1]]); 
    visualizeMap(occupancyMap, robotPos);
    time.sleep(0.1);
    prevScan = newScan; 
    

'''for i in data:
    scan = convertScanToXY(i);
    occupancyMap = insertPoints(scan, occupancyMap);
    visualizeMap(occupancyMap, np.array([0,0])); 
    time.sleep(0.1);'''
