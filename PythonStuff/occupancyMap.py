import matplotlib.pyplot as plt
import numpy as np



def initMap():
    #scale 1 unit = 1cm = 0.01m 
    occupancyMap = np.zeros([10000,10000]); 
    return occupancyMap;

def convertWorldFrameToMap(points, occupancyMap):
    offset = len(occupancyMap)/2;
    points = (points) + offset;
    points = points.astype('int'); 
    return points;

def insertPoints(pointsWorldFrame, occupancyMap):
    #points -> 2d array of points in world frame 
    pointsMap = convertWorldFrameToMap(pointsWorldFrame, occupancyMap);
    occupancyMap[pointsMap[:,0], pointsMap[:,1]] = 1;
    return occupancyMap;

def visualizeMap(occupancyMap):
    fig = plt.figure(1);
    ax = fig.add_subplot(111);
    ax.imshow(occupancyMap, cmap='Greys');
    fig.canvas.draw()
    plt.show(block=False)

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

