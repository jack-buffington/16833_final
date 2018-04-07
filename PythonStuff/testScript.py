from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
import time

data = loadData('scanData.txt')
occupancyMap = initMap(); 
for i in data:
    scan = convertScanToXY(i);
    occupancyMap = insertPoints(scan, occupancyMap);
    visualizeMap(occupancyMap); 
    time.sleep(0.1);
