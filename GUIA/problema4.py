import threading as th

contador =[0,0]

def hilo(num):
	for i in range(1,11):
		t=num
		print(f"Hilo {num} valor de {i}",flush=True)
		other = contador[1-t]
		contador[t]=other +1

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
