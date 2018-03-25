import numpy as np
import math

def distance(x1,y1,x2,y2):
    dist=math.sqrt(((float(x1)-float(x2))*(float(x1)-float(x2)))+((float(y1)-float(y2))*(float(y1)-float(y2))))
    return dist

def findCentroid(points):
    n=len(points)
    points=np.array(points)
    sum_x=np.sum(points[:,0])
    sum_y=np.sum(points[:,-1])
    x=float(sum_x/n)
    y=float(sum_y/n)
    return np.array([x,y])

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

#if __name__=="__main__":
    
            
            
