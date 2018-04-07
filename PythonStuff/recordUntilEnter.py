#!/usr/bin/env python3
'''Animates distances and measurment quality'''

# You may need to run this several times before it works....


from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import time
import thread



PORT_NAME = '/dev/ttyUSB1'
DMAX = 4000
IMIN = 0
IMAX = 50

def input_thread(a_list):
    raw_input()  # Stalls waiting for input
    a_list.append(True)

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,


def run():

    count = 1
    print '\n\n\nThis program will terminate when you hit enter'
    # time.sleep(1.5)

    a_list = []
    thread.start_new_thread(input_thread, (a_list,))

    lidar = RPLidar(PORT_NAME)

    iterator = lidar.iter_measurments() 

    #currentList = 0
    foundFirstNewScan = False

    data = []

    for I in iterator:

        # Scan for the new scan flag
        if I[0] == True:
            # Check for the enter key to have been pressed
            try:
                A = a_list[0]
                print 'Writing data to disk...'
                thefile = open('scanData02.txt', 'w')


                for item in data:
                    thefile.write("%s\n" % item)

                lidar.stop()
                lidar.disconnect()
                print 'Done!'

                break
            except:
                pass

            if foundFirstNewScan == False:
                foundFirstNewScan = True
                print 'Starting to scan...'
            else:
                data.append(temp)
                # currentList += 1
                # print 'Current scan: ', currentList
                # if currentList == 10:
                #     break
            temp = [] # This is the array that will hold a scan

        if foundFirstNewScan == True:
            temp.append([I[2], I[3]])


        #print 'new: ', I[0], '   quality: ', I[1], '   angle: ', I[2], '   distance: ', I[3]   

    # print 'Writing data to disk...'
    # thefile = open('scanData01.txt', 'w')


    # for item in data:
    #     thefile.write("%s\n" % item)

    # lidar.stop()
    # lidar.disconnect()
    # print 'Done!'

if __name__ == '__main__':
    run()