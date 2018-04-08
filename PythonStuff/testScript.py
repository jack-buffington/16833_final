from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
import time
import numpy as np

data = loadData('scanData.txt')
occupancyMap = initMap(); 
for i in data:
    scan = convertScanToXY(i);
    occupancyMap = insertPoints(scan, occupancyMap);
    visualizeMap(occupancyMap, np.array([0,0])); 
    time.sleep(0.1);
