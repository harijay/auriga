#!/usr/bin/python3.1
# -*- coding: latin-1 -*-
# Class that takes in a file name and other optional inputs and converts the scafile to an mtz file
from optparse import OptionParser
import aurigaerrors
import os
import sys
import subprocess
from Queue import Queue
from threading import Thread
import threading
from mrdict import modeldict
import shlex
import tempfile
from process_multi_util_functions import report,safe_write_script
from scatomtzrunthread import ScaToMtzRunThread
from refmac5runthread import Refmac5RunThread
from phaserrunthread import PhaserRunThread


auriga_output_directory_root = None
THREAD_COUNT = 8


scafile_in_queue = Queue()
phaser_in_queue = Queue()
refmac5_in_queue = Queue()
refmac5_out_queue = Queue()

def main():
    my_option_parser = OptionParser()
    my_option_parser.add_option("--scafiles_list","-s",metavar=["Scafiles txt list"],dest="scalist",default="scafiles.txt")
    options,args = None,None
    
    if len(sys.argv) == 1:
        my_option_parser.print_help()
        exit()
    else:    
        try:
            (options,args) = my_option_parser.parse_args()
            print ("Options", options)
        except IndexError:
            my_option_parser.print_help()
    
    # Check and see if the global output directory is defined
    
    if os.environ.get("AURIGA_OUTPUT_ROOT"):
        auriga_output_directory_root=os.environ.get("AURIGA_OUTPUT_ROOT")
    else:
        auriga_output_directory_root=os.path.abspath(os.curdir)
            
    sca_listfile = options.scalist
    
    for i in open(sca_listfile,"r"):
        scafile_in_queue.put(i)        
    thread_list  = []
    
    for i in range(THREAD_COUNT):
        scala_worker = ScaToMtzRunThread(scafile_in_queue, phaser_in_queue,auriga_output_directory_root)
        phaser_worker = PhaserRunThread(phaser_in_queue,refmac5_in_queue,auriga_output_directory_root)
        refmac5_worker = Refmac5RunThread(refmac5_in_queue,refmac5_out_queue,auriga_output_directory_root)
        thread_list.append(scala_worker)
        thread_list.append(phaser_worker)
        thread_list.append(refmac5_worker)

    for worker in thread_list:
        worker.start()
    
if __name__ == '__main__':
    main()
    
# Global output directory root prefix

            



    

    

            
