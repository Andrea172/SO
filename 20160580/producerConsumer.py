import threading as th


global n
global indice

buffer = [None,None,None,None,None,None,None,None]

def productor(c):
	global n
	while True:
		with c:
			global indice
			global buffer
			item = (n*n)%100
			n+=1
			if (buffer[indice]!=None):
				c.wait()
			indice=(indice+1)%8
			buffer[indice]=item
			print(f"productor {indice} {item} {buffer}", flush = True)
			if (buffer[indice]!=None):
				c.notify()

def consumidor(c):
	item = None
	while True:
		with c:
			global indice
			global buffer
			if (buffer[indice]==None):
				c.wait()
			item = buffer[indice]
			buffer[indice]=None
			print(f"consumidor {indice} {item} {buffer}",flush = True)
			indice =(indice-1)%8
			if (buffer[indice]==None):
				c.notify()


c = th.Condition()
n=0
indice = -1
for _ in range(4):
	t=th.Thread(target=productor,args=(c,))
	t.start()
for _ in range(4):
	t=th.Thread(target=consumidor,args=(c,))
	t.start()