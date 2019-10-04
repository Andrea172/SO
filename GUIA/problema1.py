import threading as th

def hilo(num):
	print(f"Hi, congratulations you are running your first threading program, i am thread {num}.")
	print(f"Python threads are used in cases where the execution of a task involves some waiting, i am thread {num}.")
	print(f"Threading allows python to execute other code while waiting, i am thread {num}.")

hilos=[]
for n in range(4):
	h = th.Thread(target=hilo,args=(n,))
	hilos.append(h)

for n in range(4):
	hilos[n].start()