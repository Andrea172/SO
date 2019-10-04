import threading as th

global a
a=0

def line1():
	global a
	while(a!=2): pass
	e1.acquire()
	print("Operativos")
	e1.release()

def line2():
	global a
	print("INF",end=' ')
	a+=1


def line3():
	global a
	while(a!=1): pass
	e1.acquire()
	a+=1
	print("Sistemas",end=' ')
	e1.release()

e1 = th.Condition()

t=th.Thread(target = line3)
t.start()
t=th.Thread(target = line2)
t.start()
t=th.Thread(target = line1)
t.start()