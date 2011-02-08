from refmac5runscriptcreator import Refmac5RunScriptCreator
from threading import Thread
import subprocess
import time
import os
from process_multi_util_functions import safe_write_script
class Refmac5RunThread(Thread):

    def __init__(self,in_queue,out_queue,auriga_output_directory_root):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.auriga_output_directory_root = auriga_output_directory_root

    def create_coot_start_script(self,dir_for_scr,output_file_root):
        script_location = os.path.join(dir_for_scr ,"coot_start.sh")
        cootscr = open(script_location,"w")
        coot_str = """#!/bin/bash\n
        coot --auto {output_file_root}.2.mtz --pdb {output_file_root}.2.pdb""".format(output_file_root = output_file_root)
        print coot_str
        safe_write_script(coot_str,cootscr)
        
        
    def run(self):
        while True:
            my_mtz = self.in_queue.get()
            if my_mtz == None:
                self.out_queue.put(None)
                self.in_queue.task_done()
                break
            refmac5_run_object = Refmac5RunScriptCreator(my_mtz,self.auriga_output_directory_root)
            runscript = refmac5_run_object.write_runscript_and_return_name()
            try:
	    	subprocess.check_call([runscript],close_fds=True,bufsize=0)
            except subprocess.CalledProcessError:
                self.in_queue.put(my_mtz)
                continue
                #                self.in_queue.task_done()
            except OSError:
                self.in_queue.put(my_mtz)
                continue
                #                self.in_queue.task_done()
            self.out_queue.put(my_mtz)
            self.create_coot_start_script(refmac5_run_object.proj_name,refmac5_run_object.phaseroutput_root)
            self.in_queue.task_done()

