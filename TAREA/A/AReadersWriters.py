import threading as th
import time 

def Writer():
	roomEmpty.acquire()
	print("writing")
	roomEmpty.release()

def Reader():
	global readers
	mutex.acquire()
	readers +=1
	if readers == 1:
		roomEmpty.acquire() 
	mutex.release()
	print("Reading")
	mutex.acquire()
	readers -=1
	if readers == 0:
		roomEmpty.release()
	mutex.release()


readers = 0
mutex = th.Semaphore(1)
roomEmpty = th.Semaphore(1)

for i in range(3):
	t = th.Thread(target=Writer)
	t.start()
	t2 = th.Thread(target=Reader)
	t2.start()