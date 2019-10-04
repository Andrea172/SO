import threading as th

def line1():
	e2.wait()
	print("Operativos")

def line2():
	print("INF",end=' ')
	e1.set()

def line3():
	e1.wait()
	print("Sistemas",end=' ')
	e2.set()

e1 = th.Event()
e1.clear()
e2 = th.Event()
e2.clear()

t=th.Thread(target = line1)
t.start()
t=th.Thread(target = line2)
t.start()
t=th.Thread(target = line3)
t.start()

