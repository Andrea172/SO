import threading
global barrierCollectToLog
global barrierCollectToStat
global barrierLog
global barrierStat
global barrierReport
global barrierStatToCollect

barrierCollectToStat = threading.Barrier(2)
barrierCollectToLog = threading.Barrier(2)
barrierStat = threading.Barrier(2)
barrierReport = threading.Barrier(2)
barrierStatToCollect = threading.Barrier(2)
barrierLog = threading.Barrier(2)

def Collect():
  global barrierStatToCollect
  global barrierLog
  global barrierCollect
  while True:
      barrierStatToCollect.wait()
      barrierLog.wait()
      print('C',end=' ')
      barrierCollectToStat.wait()
      barrierCollectToLog.wait()

def Log():
  global barrierCollectToLog
  global barrierLog
  while True:
      barrierCollectToLog.wait()
      print('L',end=' ')
      barrierLog.wait()

            
def Stat():
  global barrierCollectToStat
  global barrierReport
  global barrierStat
  global barrierStatToCollect
  while True:     
      barrierCollectToStat.wait()
      barrierReport.wait()
      print('S',end=' ')
      barrierStatToCollect.wait()
      barrierStat.wait()
      
def Report():
  global barrierStat
  global barrierReport
  while True:     
      barrierStat.wait()   
      print('R',end=' ')
      barrierReport.wait()
        
if __name__ == "__main__":
  h1=threading.Thread(target=Collect)
  h2=threading.Thread(target=Log)       
  h3=threading.Thread(target=Stat)       
  h4=threading.Thread(target=Report)
  h1.start()
  h2.start()
  h3.start()
  h4.start()
  barrierStatToCollect.wait()
  barrierLog.wait()
  barrierReport.wait()
       