from refmac5runscriptcreator import Refmac5RunScriptCreator
from threading import Thread
import subprocess
import time

class Refmac5RunThread(Thread):

    def __init__(self,in_queue,out_queue,auriga_output_directory_root):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.auriga_output_directory_root = auriga_output_directory_root
        
    def run(self):
        while True:
            my_mtz = self.in_queue.get()
#            if my_mtz is None:
#                self.in_queue.task_done()
#                self.join()
            runscript = Refmac5RunScriptCreator(my_mtz,self.auriga_output_directory_root).write_runscript_and_return_name()
            subprocess.call([runscript])
            time.sleep(2)
            self.out_queue.put(my_mtz)
