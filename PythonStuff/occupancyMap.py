import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pdb


def initMap():
    #scale 1 unit = 1cm = 0.01m 
    occupancyMap = np.zeros([100,100],dtype=int);
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
        xMax = mapSize-1;
        
    yMin = robotY - radius;
    if (yMin < 0):
        yMin = 0;
        
    yMax = robotY + radius;
    if (yMax >= mapSize):
        yMax = mapSize-1;

    xMin = int(xMin);
    xMax = int(xMax);
    yMin = int(yMin);
    yMax = int(yMax);
    validSection = np.asarray(zip(*np.where(occupancyMap==1))); #get occupied indicies in occupancy map
    validIndices = np.zeros((len(validSection))); 
    for i in range(len(validSection)):
        x = validSection[i,0];
        y = validSection[i,1];
        #points which are within the reqd range have the index set to 1 in valid indices
        if ( x>=xMin & x<=xMax & y>=yMin & y<=yMax):
            validIndices[i] = 1;
    validIndices = np.where(validIndices==1);
    mapSectionXY = validSection[validIndices];
    mapSectionXY = convertMapToWorldFrame(mapSectionXY, occupancyMap);
    #return 2D array of map points within the radius in world coordinates 
    return (mapSectionXY*10.0); 
    


def reInsertPoints(pointsWorldFrame, occupancyMap):
    #print 'reinserting points \n'
    #points -> 2d array of points in world frame 
    pointsMap = convertWorldFrameToMap(pointsWorldFrame, occupancyMap);
    if(len(pointsMap) > 0):
        occupancyMap[pointsMap[:,0], pointsMap[:,1]] = int(1);
    return occupancyMap;

def expandMap(occupancyMap):
    offset = 200; 
    #print 'expanding map \n'
    mapSize = len(occupancyMap);
    #pdb.set_trace()
    occupiedPoints = np.asarray(zip(*np.where(occupancyMap==1)));
    occupiedPointsWorldFrame = convertMapToWorldFrame(occupiedPoints, occupancyMap);
        
    newMapSize = mapSize + offset;
    #print newMapSize
    newOccupancyMap = np.zeros([newMapSize, newMapSize], dtype=int);
    newOccupancyMap = reInsertPoints(occupiedPointsWorldFrame, newOccupancyMap);
    return newOccupancyMap;

def withinMap(points, occupancyMap):
    #print 'in withinMap function'
    mapSize = len(occupancyMap);
    outOfMaxBounds = zip(*np.where(points > (mapSize-1)));
    outOfMinBounds = zip(*np.where(points < 0));
    if (len(outOfMaxBounds)==0 and len(outOfMinBounds) ==0):
        return True;
    else:
        return False; 

    
def insertPoints(pointsWorldFrame, occupancyMap):
    #points -> 2d array of points in world frame
    #print 'Inserting new points'
    pointsMapFrame = convertWorldFrameToMap(pointsWorldFrame, occupancyMap);
    while(withinMap(pointsMapFrame, occupancyMap) == False):
        occupancyMap = expandMap(occupancyMap);
        pointsMapFrame = convertWorldFrameToMap(pointsWorldFrame, occupancyMap);
    
    occupancyMap[pointsMapFrame[:,0], pointsMapFrame[:,1]] = int(1);
    return occupancyMap;

def visualizeMap(occupancyMap, robotPos):
    #robot pose in world coordinates 
    fig = plt.figure(1);
    ax = fig.add_subplot(111);
    ax.clear(); 
    offset = len(occupancyMap)/2;
    #find where in the occupancyMap is filled, return as an (x,y) 2D array 
    occMapXY = np.asarray(zip(*np.where(occupancyMap==1)));
    ax.scatter( occMapXY[:,1],occMapXY[:,0], c='b', marker='.',s=10); 
    ax.scatter(robotPos[:,1]+offset, robotPos[:,0]+offset, c='r', s=5);
    #plt.xlim(0,len(occupancyMap));
    #plt.ylim(0,len(occupancyMap));
    plt.axis('equal'); 
    fig.canvas.draw();
    plt.show(block=False);

def visualizeScan(points, clearFlag,color):
    fig = plt.figure(2);
    ax = fig.add_subplot(111); 
    if (clearFlag):
        ax.clear();
    x = points[:,0];
    y = points[:,1]; 
    ax.scatter(y,x,c=color);
    plt.axis('equal');
    fig.canvas.draw();
    fig.canvas.flush_events(); 
    plt.show(block=False);

