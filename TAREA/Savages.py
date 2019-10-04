import threading as th
cont=0
M=4
def Savage():
	global cont
	global M
	while True :
		lleno.acquire()
		print("COMER")
		cont+=1
		if(cont==M):
			empty.release()
		else:
			lleno.release()

def Cook():
	global cont
	for _ in range(5):
		empty.acquire()
		print("LLENAR OLLA")
		cont=0
		lleno.release()


empty = th.Semaphore(1)
lleno = th.Semaphore(0)

t = th.Thread(target=Cook)
t.start()

for i in range(5):
	t1 = th.Thread(target=Savage)
	t1.start()