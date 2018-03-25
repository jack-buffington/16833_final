import numpy

#The .txt file stores the numbers as strings. To convert it to a float array,
#each line need to have the square brackets, spaces and commas removed. Then
#the result of that extraction can then be converted to a float array. 

def loadData(path):
    data = list(); 
    with open(path, 'rt') as dataFile:
        #read each line
        for line in dataFile:
            #replace each square bracket and comma with a space
            strippedLine = line.replace('[','').replace(']','').replace(',','').replace('\n',''); 
            #strippedLine = strippedLine.split(' ');
            ''' = [val for val in strippedLine if val!=''];
            scan = scan[0:-1];
            scan = np.asarray(scan, dtype='float');
            scan = scan.reshape(len(scan)/2, 2); 
            data.append(scan); '''
    return strippedLine

data = loadData("scanData.txt"); 
            
