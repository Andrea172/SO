import threading as th

indice = -1
buffer = [None,None,None,None,None]

def productor():
	for n in range(20):
		global indice
		global buffer
		item = n*n
		if indice < 5:
			indice +=1
			buffer[indice]=item
			print(f"productor {indice} {item} {buffer}", flush = True)

def consumidor():
	item = None
	for _ in range(20):
		global indice
		global buffer
		if indice > -1:
			item = buffer[indice]
			buffer[indice]=None
			print(f"consumidor {indice} {item} {buffer}",flush = True)
			indice -=1

t=th.Thread(target=productor)
t.start()
t=th.Thread(target=consumidor)
t.start()