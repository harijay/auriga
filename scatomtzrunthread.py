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
        sys.excepthook = self.report_error
        
    def report_error(type=None,value=None,traceback=None):
        if type is OSError:
            print ("***FilenameError***",value.filename)
            sys.__excepthook__(type,value,traceback)
        else:
            sys.__excepthook__(type,value,traceback)

            
    def run(self):
        while True:
            path = self.in_queue.get()
            myfile = ScalePackToMtzRunscriptCreator(path,self.auriga_output_directory_root)
            scrfile = myfile.create_and_return_runscript_file()
            time.sleep(2)
	    try:
                subprocess.Popen([scrfile],close_fds=True).wait()
                time.sleep(2)
            except subprocess.CalledProcessError:
                self.in_queue.put(path)
            except OSError:
                self.in_queue.put(path)
	    self.out_queue.put(myfile.mtzoutpath())
            self.in_queue.task_done()
            
