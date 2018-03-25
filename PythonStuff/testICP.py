import numpy as np 
from dataFileParser import loadData
from ICP import ICP

data = loadData("scanData.txt"); 

oldScan = np.array(data[0])
newScan = np.array(data[1])

translation,rotationMatrix = ICP(oldScan,newScan)

print 'translation: ', translation
print 'rotation matrix: '
print  rotationMatrix
