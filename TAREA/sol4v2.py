import threading as th

contador =[0,0]
cont1=0
cont2=0
def hilo(num,):
	global cont1
	global cont2
	for i in range(1,11):
		t=num
		print(f"Hilo {num} valor de {i}",flush=True)
		other = contador[1-t]
		b.acquire()
		if cont1==0:
			cont1+=1
			b.wait()
		if cont1==1:
			b.notify()
			cont1=0
		b.release()
		contador[t]=other +1
		b.acquire()
		if cont2==0:
			cont2+=1
			b.wait()
		if cont2==1:
			b.notify()
			cont2=0
		b.release()

b = th.Condition()

ths = []
for i in range(2):
	t=th.Thread(target=hilo, args=(i,))
	ths.append(t)

for i in range(2):
	ths[i].start()

for i in range(2):
	ths[i].join()

print(f"contado de hilo 0 {contador[0]}")
print(f"contado de hilo 1 {contador[1]}")