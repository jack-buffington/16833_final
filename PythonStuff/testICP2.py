import numpy as np 
from dataFileParser import loadData
from ICP2 import ICP2

data = loadData("scanData.txt"); 

oldScan = np.array(data[0])
newScan = np.array(data[1])

# translation,rotationMatrix = ICP2(oldScan,newScan)
translation,rotationMatrix = ICP2(oldScan,oldScan)

print 'translation: ', translation
print 'rotation matrix: '
print  rotationMatrix
