#!/usr/bin/env python
from phaserrunscriptcreator import PhaserRunScriptCreator
from threading import Thread
import subprocess
import sys,os
import time

class PhaserRunThread(Thread):
    def __init__(self,in_queue,out_queue,auriga_output_directory_root):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.auriga_output_directory_root = auriga_output_directory_root
        
    def run(self):
        while True:
            mtzfile = self.in_queue.get()
            phaser_run_script_creator  = PhaserRunScriptCreator(mtzfile,self.auriga_output_directory_root)
            my_phaser_script = phaser_run_script_creator.write_runscript_and_return_name()
            print ("Phaser Run Script created:%s" %  my_phaser_script)
            try:
		subprocess.check_call([my_phaser_script],close_fds=True)
            	time.sleep(2)
            except subprocess.CalledProcessError:
                self.in_queue.put(mtzfile)
            except OSError:
                self.in_queue.put(mtzfile)
            self.out_queue.put(phaser_run_script_creator.outfilepath)
 	    self.in_queue.task_done()
