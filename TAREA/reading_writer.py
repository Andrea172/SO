import threading, time
from multiprocessing import Condition


class SharedResource():
    def __init__(self):
        self.val = 0

# The class solving this problem
class RWLock:
    def __init__(self):
        self.cond = Condition()
        self.readers = 0

    def read_acquire(self):
        self.cond.acquire()
        self.readers += 1
        self.cond.release()

    def read_release(self):
        with self.cond:
            self.readers -= 1
            if (self.readers == 0):
                self.cond.notify_all()

    def write_acquire(self):
        self.cond.acquire()
        if (self.readers > 0):
            self.cond.wait()

    def write_release(self):
        self.cond.release()


def read(lock, res):
    while True:
        lock.read_acquire()
        print(threading.current_thread().ident, "Reading:",res.val)
        time.sleep(0.5)
        lock.read_release()

def write(lock, res):
    while True:
        lock.write_acquire()
        print(threading.current_thread().ident, "Writing")
        res.val += 1
        time.sleep(1)
        lock.write_release()


if __name__ == '__main__':
    lock = RWLock()
    res = SharedResource()


    for i in range(10):
        t = threading.Thread(target=write, args=(lock,res,))
        t.start()
        
    for i in range(10):
        t = threading.Thread(target=read, args=(lock,res,))
        t.start()