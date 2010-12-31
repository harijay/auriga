#!/usr/bin/python
from scalepacktomtzrunscriptcreator import ScalePackToMtzRunscriptCreator
from process_multi_util_functions import report
from threading import Thread
import sys
import subprocess
import time
import pprint

class ScaToMtzRunThread(Thread):
    def __init__(self, in_queue, out_queue,auriga_output_directory_root):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.auriga_output_directory_root = auriga_output_directory_root

    def run(self):
        while True:
            path = self.in_queue.get()
#            sys.stdout.flush()
#            if path is None:
#                self.in_queue.task_done()
#                self.join()
            myfile = ScalePackToMtzRunscriptCreator(path,self.auriga_output_directory_root)
            scrfile = myfile.create_and_return_runscript_file()
            try:
                subprocess.check_call([scrfile])
                time.sleep(2)
            except subprocess.CalledProcessError:
                self.in_queue.put(path)

            self.out_queue.put(myfile.mtzoutpath())
            
