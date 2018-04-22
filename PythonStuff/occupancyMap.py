import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pdb


def initMap():
    #scale 1 unit = 1cm = 0.01m 
    occupancyMap = np.zeros([10000,10000]); 
    return occupancyMap;


    

def convertWorldFrameToMap(points, occupancyMap):
    offset = len(occupancyMap)/2;
    points = (points) + offset;
    points = points.astype('int'); 
    return points;

def convertMapToWorldFrame(points, occupancyMap):
    offset = len(occupancyMap)/2;
    points = (points) - offset;
    return points;


    
def getPointsWithinRadius(occupancyMap, robotPose, radius):
    #radius in centimetres.
    #robot pose in world Coordinates
    mapSize = len(occupancyMap);
    offset = mapSize/2; 
    robotX = robotPose[0]+offset;
    robotY = robotPose[1]+offset;
    
    xMin =  robotX - radius;
    if (xMin < 0):
        xMin = 0;
        
    xMax = robotX + radius;
    if (xMax >= mapSize):
        xMax = mapSize;
        
    yMin = robotY - radius;
    if (yMin < 0):
        yMin = 0;
        
    yMax = robotY + radius;
    if (yMax >= mapSize):
        yMax = mapSize;

    mapSection = occupancyMap[xMin:xMax, yMin:yMax];
    mapSectionXY = np.asarray(zip(*np.where(mapSection==1)));
    mapSectionXY = convertMapToWorldFrame(mapSectionXY, occupancyMap); 
    return mapSectionXY; 
    


def reInsertPoints(pointsWorldFrame, occupancyMap):
    #print 'reinserting points \n'
    #points -> 2d array of points in world frame 
    pointsMap = convertWorldFrameToMap(pointsWorldFrame, occupancyMap);
    if(len(pointsMap) > 0):
        occupancyMap[pointsMap[:,0], pointsMap[:,1]] = 1;
    return occupancyMap;

def expandMap(occupancyMap):
    #print 'expanding map \n'
    mapSize = len(occupancyMap);
    occupiedPoints = np.asarray(zip(*np.where(occupancyMap==1)));
    occupiedPointsWorldFrame = convertMapToWorldFrame(occupiedPoints, occupancyMap);
        
    newMapSize = 5*mapSize;
    newOccupancyMap = np.zeros([newMapSize, newMapSize]);
    newOccupancyMap = reInsertPoints(occupiedPointsWorldFrame, newOccupancyMap);
    return newOccupancyMap;

def withinMap(points, occupancyMap):
    mapSize = len(occupancyMap);
    outOfMaxBounds = zip(*np.where(points > (mapSize-1)));
    outOfMinBounds = zip(*np.where(points < 0));
    if (len(outOfMaxBounds)==0 and len(outOfMinBounds) ==0):
        return True;
    else:
        return False; 

    
def insertPoints(pointsWorldFrame, occupancyMap):
    #points -> 2d array of points in world frame 
    pointsMap = convertWorldFrameToMap(pointsWorldFrame, occupancyMap);
    
    while(withinMap(pointsMap, occupancyMap) == False):
        occupancyMap = expandMap(occupancyMap);
        pointsMap = convertWorldFrameToMap(pointsWorldFrame, occupancyMap);
    
    occupancyMap[pointsMap[:,0], pointsMap[:,1]] = 1;
    return occupancyMap;

def visualizeMap(occupancyMap, robotPos):
    #robot pose in world coordinates 
    fig = plt.figure(1);
    ax = fig.add_subplot(111);
    offset = len(occupancyMap)/2;
    #find where in the occupancyMap is filled, return as an (x,y) 2D array 
    occMapXY = np.asarray(zip(*np.where(occupancyMap==1)));
    ax.scatter(occMapXY[:,0], occMapXY[:,1], c='b', marker='.'); 
    ax.scatter(robotPos[0]+offset, robotPos[1]+offset, c='r', marker='8'); 
    plt.xlim(0,10000);
    plt.ylim(0,10000);
    #plt.axis('equal'); 
    fig.canvas.draw();
    plt.show(block=False);

def visualizeScan(points, clearFlag):
    fig = plt.figure(1);
    ax = fig.add_subplot(111); 
    if (clearFlag):
        ax.clear();
    x = points[:,0];
    y = points[:,1]; 
    ax.scatter(x,y);
    plt.axis('equal');
    fig.canvas.draw(); 
    plt.show(block=False);
