import threading as th

isTobacco = isPaper = isMatch = False

def Pusher():
	while (True):
		PusherA()
		PusherB()
		PusherC()

def agentA():
	agentSem.acquire()
	tobacco.release()
	paper.release()

def agentB():
	agentSem.acquire()
	tobacco.release()
	match.release()

def agentC():
	agentSem.acquire()
	match.release()
	paper.release()	

def PusherA():
	global isPaper
	global isMatch
	global isTobacco
	tobacco.acquire()
	mutex.acquire()
	if isPaper:
		isPaper= False
		matchSem.release()
	elif isMatch:
		isMatch = False
		paperSem.release()
	else:
		isTobacco = True
	mutex.release()

def PusherB():
	global isPaper
	global isMatch
	global isTobacco
	paper.acquire()
	mutex.acquire()
	if isMatch:
		isMatch = False
		tobaccoSem.release()
	elif isTobacco:
		isTobacco = False
		matchSem.release()
	else:
		isPaper = True
	mutex.release()

def PusherC():
	global isPaper
	global isMatch
	global isTobacco
	match.acquire()
	mutex.acquire()
	if isTobacco:
		isTobacco= False
		paperSem.release()
	elif isPaper:
		isPaper = False
		tobaccoSem.release()
	else:
		isMatch = True
	mutex.release()

def SmokerTobacco():
	tobaccoSem.acquire()
	print("TOBACCO Cigarette in process")
	agentSem.release()
	print("Smoke")

def SmokerPaper():
	paperSem.acquire()
	print("PAPER Cigarette in process")
	agentSem.release()
	print("Smoke")

def SmokerMatch():
	matchSem.acquire()
	print("MATCH Cigarette in process")
	agentSem.release()
	print("Smoke")

agentSem = th.Semaphore(1)
tobacco = th.Semaphore(0)
paper = th.Semaphore(0)
match = th.Semaphore(0)
mutex = th.Semaphore(1)
tobaccoSem = th.Semaphore(0)
paperSem = th.Semaphore(0)
matchSem = th.Semaphore(0)


t2 = th.Thread(target=agentA)
t2.start()

t2 = th.Thread(target=agentB)
t2.start()

t6 = th.Thread(target=agentC)
t6.start()

t = th.Thread(target=SmokerMatch)
t.start()

t3 = th.Thread(target=Pusher)
t3.start()

t4 = th.Thread(target=SmokerPaper)
t4.start()

t5 = th.Thread(target=SmokerTobacco)
t5.start()
