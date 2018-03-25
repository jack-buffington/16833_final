import numpy as np

'''
The .txt file stores the numbers as strings. To convert it to a float array,
each line need to have the square brackets, spaces and commas removed. Then
the result of that extraction can then be converted to a float array.

The output is data which is list. Each element of the list is a 2D float array. 
Each floar array represents a batch on scans.For example scan0 = data[0]. 
scan0[0,0] is the angle measurement, and scan0[0,1] is the range measurement. 
'''

def loadData(path):
    data = list(); 
    with open(path, 'rt') as dataFile:
        #read each line
        for line in dataFile:
            #replace each square bracket, comma and EOL token with nothing
            strippedLine = line.replace('[','').replace(']','').replace(',','').replace('\n',''); 
            scan = strippedLine.split(' ');
            scan = np.asarray(scan, dtype='float');
            scan = scan.reshape(len(scan)/2, 2); 
            data.append(scan); 
    return data


            
