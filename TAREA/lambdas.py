
def predicado(a):
	return a >= 8

lista = [1,2,3,4,5]

map(lambda x: x+=1, lista)

def evaluar():
	a = 8
	with condition:
		condition.wait_for(lambda: predicado(a))
		print("despierto y continuando")

def otro_evaluando():
	with condition:
		condition.notify_all()