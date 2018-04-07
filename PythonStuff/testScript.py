from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
import time

data = loadData('scanData.txt')
for i in data:
    scan = convertScanToXY(i);
    visualizeScan(scan, True);
    time.sleep(0.1);
    print i
