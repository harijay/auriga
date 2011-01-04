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
        while not self.in_queue.empty():
            my_mtz = self.in_queue.get()
            runscript = Refmac5RunScriptCreator(my_mtz,self.auriga_output_directory_root).write_runscript_and_return_name()
            try:
	    	subprocess.check_call([runscript],close_fds=True,bufsize=0)
            except subprocess.CalledProcessError:
                self.in_queue.put(my_mtz)
                #                self.in_queue.task_done()
            except OSError:
                self.in_queue.put(my_mtz)
                #                self.in_queue.task_done()
            self.out_queue.put(my_mtz)
            self.in_queue.task_done()

