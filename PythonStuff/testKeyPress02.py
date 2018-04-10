import thread
import time


count = 1


def input_thread(a_list):
	raw_input()  # Stalls waiting for input

	a_list.append(True)


a_list = []
thread.start_new_thread(input_thread, (a_list,))


print '\n\n\nThis program will terminate when you hit enter'
time.sleep(1.5)

while True:
    print count
    count += 1
    time.sleep(.05)
    try:
    	A = a_list[0]
    	break
    except:
    	pass

print('Done!')
