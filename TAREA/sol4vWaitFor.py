import threading as th

contador =[0,0]
cont=0


def evaluadora():
	global cont
	cont=cont+1
	if(cont==1):
		return False
	if(cont==2):
		b.notify()
		cont=0
		return True

def hilo(num,cv):
	global cont
	global contador
	for i in range(1,11):
		with cv:
			t=num
			print(f"Hilo {num} valor de {i}",flush=True)
			other = contador[1-t]
			b.wait_for(evaluadora)

			contador[t]=other +1
			b.wait_for(evaluadora)
			print(f"contador del hilo {num} es {contador[t]}")



b = th.Condition()

ths = []
for i in range(2):
	t=th.Thread(target=hilo, args=(i,b))
	ths.append(t)

for i in range(2):
	ths[i].start()

for i in range(2):
	ths[i].join()

print(f"contado de hilo 0 {contador[0]}")
print(f"contado de hilo 1 {contador[1]}")