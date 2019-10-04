import threading as th


def Hidrogeno():
	cont=0
	while True:
		iniciar.wait()
		cont+=1
		mutex.acquire()
		print("H",end="")
		if (cont==2):
			cont=0
			iniciar.clear()
			finalH.set()
		mutex.release()

def Oxigeno():
	while True:
		iniciarO.wait()
		mutex.acquire()
		iniciarO.clear()
		print("O",end="")
		cambio.set()
		mutex.release()

def CambiodeLinea():
	while True:
		cambio.wait()
		finalH.wait()
		mutex.acquire()
		cambio.clear()
		finalH.clear()
		print()
		iniciar.set()
		iniciarO.set()
		mutex.release()

iniciar = th.Event()
iniciar.clear()
iniciar.set()
iniciarO = th.Event()
iniciarO.clear()
iniciarO.set()
cambio = th.Event()
cambio.clear()
finalH = th.Event()
finalH.clear()
mutex = th.Semaphore(1)
t = th.Thread(target=Hidrogeno)
t.start()
t = th.Thread(target=Oxigeno)
t.start()
t = th.Thread(target=CambiodeLinea)
t.start()