import threading as th
import time 

def barber():
	global n
	global countC
	global queue
	while(True):
		sCustomer.acquire()
		mutex.acquire()
		sem = queue.pop(0)
		mutex.release()
		sem.release()
		print("Cutting the hair")
		sCustomerDone.acquire()
		sBarberDone.release()

def customer():
	global n
	global countC
	global queue
	sem = th.Semaphore(0)

	mutex.acquire()
	if (countC<n):
		countC+=1
		queue.append(sem)
	else:
		print("No hay espacio")
		mutex.release()
		return
	mutex.release()
	sCustomer.release()
	sem.acquire()
	print("The barber is cutting my hair")
	sCustomerDone.release()
	sBarberDone.acquire()
	mutex.acquire()
	countC-=1
	mutex.release()

	

mutex = th.Semaphore(1)
sCustomer = th.Semaphore(0)
sBarberDone = th.Semaphore(0)
sCustomerDone = th.Semaphore(0)
n=4
countC=0
queue=[]

t2 = th.Thread(target=barber)
t2.start()

for i in range(5):
	t = th.Thread(target=customer)
	t.start()
