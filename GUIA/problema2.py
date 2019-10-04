import threading as th

def line1():
	print("Operativos")

def line2():
	print("INF",end=' ')

def line3():
	print("Sistemas",end=' ')

t=th.Thread(target = line1)
t.start()
t=th.Thread(target = line2)
t.start()
t=th.Thread(target = line3)
t.start()

