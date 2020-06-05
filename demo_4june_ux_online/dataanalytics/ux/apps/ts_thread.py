import threading
import os
from dataanalytics.framework.file_utils import FileUtils

class TSThread(threading.Thread):

   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self):
      msg = '$$RUN Time Series Analysis Thread : ' + self.name
      print(msg)
      os.system('pwd')
      path = os.path.join('dataanalytics', 'ts')
      path = os.path.join(path, 'Landing_Page.py')
      cmd = 'python3 '+ path
      print(cmd)
      os.system(cmd)
      msg = '$$RUN Time Series Analysis Thread Task Completed : ' + self.name
      print(msg)
