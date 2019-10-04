import threading as th

indice = -1
buffer = [None,None,None,None,None]

def productor(cv):
	for n in range(20):
		with cv:
			global indice
			global buffer
			item = n*n
			while (indice>=4):
				c.wait()
			indice +=1
			buffer[indice]=item
			print(f"productor {indice} {item} {buffer}", flush = True)
			if (indice>-1):
				c.notify()

def consumidor(cv):
	item = None
	for _ in range(20):
		with cv:
			global indice
			global buffer
			while (indice<=-1):
				c.wait()
			item = buffer[indice]
			buffer[indice]=None
			print(f"consumidor {indice} {item} {buffer}",flush = True)
			indice -=1
			if (indice<4):
				c.notify()


c = th.Condition()

t=th.Thread(target=productor,args=(c,))
t.start()
t=th.Thread(target=consumidor,args=(c,))
t.start()