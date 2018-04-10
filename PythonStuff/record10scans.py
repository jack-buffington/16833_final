#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = '/dev/ttyUSB1'
DMAX = 4000
IMIN = 0
IMAX = 50



def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,


def run():
    lidar = RPLidar(PORT_NAME)

    iterator = lidar.iter_measurments() 

    currentList = 0
    foundFirstNewScan = False

    data = []

    for I in iterator:

        # Scan for the new scan flag
        if I[0] == True:
            if foundFirstNewScan == False:
                foundFirstNewScan = True
                print 'First scan'
                
            else:  # It found the beginning of a new scan
                data.append(temp)
                currentList += 1
                print 'Current scan: ', currentList
                if currentList == 10:
                    break
            temp = [] # This is the array that will hold a scan


        if foundFirstNewScan == True:
            temp.append([I[2], I[3]])


        #print 'new: ', I[0], '   quality: ', I[1], '   angle: ', I[2], '   distance: ', I[3]   

    thefile = open('scanData.txt', 'w')


    for item in data:
        thefile.write("%s\n" % item)

    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()