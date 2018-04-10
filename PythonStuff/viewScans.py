from dataFileParser import *
from convertScanToXY import *
from occupancyMap import *
import time
from ICP2 import *
from convertScanToXY import convertScanToXY


data = loadData('firstFloor.txt')
for i in data:
    scan = convertScanToXY(i);
    visualizeScan(scan, True);
    time.sleep(0.03);
    print i

# oldScan = data[0]
# newScan = data[0]

# oldScan = convertScanToXY(oldScan)
# newScan = convertScanToXY(newScan)



# visualizeScan(oldScan, False);
# visualizeScan(newScan, False);

# time.sleep(0.1);

# [rotationMatrix, translation] = ICP2(oldScan, newScan);
# print 'rotationMatrix: ', rotationMatrix
# print 'translation: ', translation
# time.sleep(1);