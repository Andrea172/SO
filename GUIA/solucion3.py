import threading as th

indice = -1
buffer = [None,None,None,None,None]

def productor():
	for n in range(20):
		global indice
		global buffer
		item = n*n
		libre.acquire()
		mutex.acquire()
		indice +=1
		buffer[indice]=item
		print(f"productor {indice} {item} {buffer}", flush = True)
		mutex.release()
		ocupado.release()

def consumidor():
	item = None
	for _ in range(20):
		global indice
		global buffer
		ocupado.acquire()
		mutex.acquire()
		item = buffer[indice]
		buffer[indice]=None
		print(f"consumidor {indice} {item} {buffer}",flush = True)
		indice -=1
		mutex.release()
		libre.release()

libre = th.Semaphore(value=5)
ocupado = th.Semaphore(value=0)
mutex = th.Semaphore(value=1)

t=th.Thread(target=productor)
t.start()
t=th.Thread(target=consumidor)
t.start()