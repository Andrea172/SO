import threading as th
import time 

def barber(i):
	global n
	global m
	global countC
	global queue
	while(True):
		sCustomer.acquire()
		mutex.acquire()
		if(len(queue)==0 and countC>n):
			queue.append(parados.pop(0))
			print(f"Me senté {i+1}")
		if(countC>0):
			sem = queue.pop(0)
		mutex.release()
		sem.release()
		print(f"B: Cutting the hair {i+1}")
		sCustomerDone.acquire()
		print(f"B: Recibiendo Pago {i+1}")
		sBarberDone.release()
		print(f"B: Recibí Pago {i+1}")

def customer(i):
	global n
	global m
	global countC
	global queue
	sem = th.Semaphore(0)

	mutex.acquire()
	if (countC<n):
		countC+=1
		queue.append(sem)
	elif(countC<m and countC>=n):
		countC+=1
		parados.append(sem)
	else:
		print(f"C: No hay espacio {i+1}")
		mutex.release()
		return
	mutex.release()
	sCustomer.release()
	sem.acquire()
	print(f"C: The barber is cutting my hair {i+1}")
	sCustomerDone.release()
	print(f"C: Pagando {i+1}")
	sBarberDone.acquire()
	mutex.acquire()
	print(f"C: Pagué {i+1}")
	countC-=1
	mutex.release()

	

mutex = th.Semaphore(1)
sCustomer = th.Semaphore(0)
sBarberDone = th.Semaphore(0)
sCustomerDone = th.Semaphore(0)
n=7
m=13
countC=0
queue=[]
parados=[]

for i in range(3):
	t2 = th.Thread(target=barber,args=(i,))
	t2.start()

for i in range(25):
	t = th.Thread(target=customer,args=(i,))
	t.start()