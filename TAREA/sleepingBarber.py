import threading
import time
import random
from multiprocessing import Process, Queue, cpu_count


def barber(queue):
    while True:
        queue.get()
        print("Barber is cutting hair")
        time.sleep(random.randint(10, 25)) # Hair cut time

def customer(queue):
	while True:
	    print("Customer in waiting room")
	    queue.put('Work')
	    time.sleep(random.randint(1, 3)) # wait for new customer to come in 


class Manager:
    def __init__(self):
        self.queue = Queue()

    def start(self):
        self.workers = [Process(target=barber, args=(self.queue,)) for i in range(3)]
        for w in self.workers:
            w.start()

        customer(self.queue)

    def stop(self):
        self.queue.put(None)
        for i in range(self.NUMBER_OF_PROCESS):
            self.workers[i].join()
        self.queue.close()


a=Manager().start()

sleep(10)

a.stop()
