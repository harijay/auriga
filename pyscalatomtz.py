#!/usr/bin/python
# Class that takes in a file name and other optional inputs and converts the scafile to an mtz file
from optparse import OptionParser
import aurigaerrors
import os
import sys
from  project_settings import auriga_proj_dir
import subprocess
from Queue import Queue
from threading import Thread,Lock

class scalatomtz(object):
    """Class that accepts filename, (optional) spacegroup,cell_dimensions, wavelength and number of residues in the ASU as imput. Runs truncate and outputs the mtz file.
    """
    
    def __init__(self,filename,spag=None,cell_dimensions_tuple=None,wavelength=None,number_of_residues_in_asu=130 ):
        """Assume only filename and infer cell dimensions and spacegroup
        """
        self.filename = filename.strip()
        self.auriga_proj_dir = auriga_proj_dir
        self.file = open(self.filename.strip(),"r")
        self.spag = self.extract_spag()
        self.cell_dimensions_string = self.extract_cell_dimensions_string()
        self.wavelength = wavelength
        self.number_of_residues_in_asu = number_of_residues_in_asu
        self.title = os.path.splitext(os.path.split(self.filename)[1])[0] + "_autoproc"
        self.proj_name =  os.path.splitext(os.path.split(self.filename)[1])[0].upper()
        self.scalepack2mtz_dict = dict(title = self.title ,spag = self.spag , cell = self.cell_dimensions_string , wavelength = self.wavelength , proj_name = self.proj_name)
        
    def extract_cell_dimensions_string(self):
        """
        
        Arguments:
        - `self`:
        """
        self.file.seek(0)
        self.file.readline()
        self.file.readline()
        cell_dimensions_string = ",".join(self.file.readline().split()[:-1])
        print "CELL DIM STR" , cell_dimensions_string
        return cell_dimensions_string
    
    def extract_spag(self):
        self.file.seek(0)
        self.file.readline()
        self.file.readline()
        cell_line =  self.file.readline().split()
        print "CELL LINE" , cell_line
        return cell_line[-1]
    
    def describe(self):
        description = """Scalepack file:{self.filename},{self.spag},{self.cell_dimensions_string}""".format(self=self)
        print description
        

    def create_and_return_runscript_file(self):
        scrfile1 = open(os.path.join(self.auriga_proj_dir,"%s_1.sh" % self.proj_name),"w")
        scrfile2 = open(os.path.join(self.auriga_proj_dir,"%s_2.sh" % self.proj_name),"w")
        scrfile3 = open(os.path.join(self.auriga_proj_dir,"%s_3.sh" % self.proj_name),"w")
        scr1 =  """#!/bin/sh
#set -e

# bug # 3192 - run-all examples produce harvest files - well to counteract
# this here set HARVESTHOME to somewhere in $CCP4_SCR

HARVESTHOME=${self.auriga_proj_dir}
export HARVESTHOME

#   from /home/hari/official_ccp4/ccp4-6.1.3/examples/unix/runnable
#   SCALEPACK2MTZ
#
#  h k l I+ SigI+ I- SigI-   were extracted from aucn.na4
#  (acentric data only), and put into scalepack format. 
#  This is simply to illustrate the procedure for getting 
#  scalepack data into CCP4. I don't really know if it
#  is a good example.
#
#  (You can use the same procedure whether or not you have 
#  anomalous data.)

scalepack2mtz hklin {self.filename}  hklout $CCP4_SCR/{self.proj_name}_junk1.mtz <<eof
name project {self.proj_name} crystal {self.proj_name} dataset {self.proj_name}
symm {self.spag}
end
eof
""".format(self = self)
        
scr2 = """#!/bin/sh
# convert Is to Fs and Ds.

truncate hklin $CCP4_SCR/{self.proj_name}_junk1.mtz hklout $CCP4_SCR/{self.proj_name}_junk2.mtz <<eof
title {self.proj_name} red aucn2 data 
truncate yes
nresidue {self.number_of_residues_in_asu}
labout  F=FP_{self.proj_name} SIGF=SIGFP_self.proj_name
end
eof
""".format(self = self)
scr3 = """#!/bin/sh
# get correct sort order and asymmetric unit

cad hklin1 $CCP4_SCR/{self.proj_name}_junk2.mtz hklout $CCP4_SCR/{self.proj_name}_trn.mtz <<eof
labi file 1 ALL
sort H K L
end
eof
#""".format(self = self)
        scrfile1.write(scr1)
        scrfile2.write(scr2)
        scrfile3.write(scr3)
        scrfile1.close()
        scrfile2.close()
        scrfile3.close()
        os.chmod(scrfile1.name,0755)
        os.chmod(scrfile2.name,0755)
        os.chmod(scrfile3.name,0755)
        
        return scrfile.name
    
#        print scrfile.name
#        mutex.acquire()
#        subprocess.call([scrfile.name])
#        sys.stdout.flush()
#        mutex.release()

def report(message):
     mutex.acquire()
     print message
     sys.stdout.flush()
     mutex.release()
     
class ScaToMtzConvertor(Thread):
    def __init__(self, in_queue, out_queue):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
    def run(self):
        while True:
            path = self.in_queue.get()
            sys.stdout.flush()
            if path is None:
                break
            print "GOTPATH" , path
            report("Converting %s" % path)
            myfile = scalatomtz(path)
            scrfile = myfile.create_and_return_runscript_file()
            subprocess.call([scrfile])
            #report(myfile.describe())
            report("Done %s" %  path)
            self.out_queue.put(path) 
            in_queue = Queue()
            
in_queue = Queue()
out_queue = Queue()
mutex = Lock()

THREAD_COUNT = 8
worker_list = []

for i in range(THREAD_COUNT):
    worker = ScaToMtzConvertor(in_queue, out_queue)
    worker.start()
    worker_list.append(worker)
    
if __name__ == '__main__':
    sca_listfile  = "scafiles.txt"
    for i in open(sca_listfile,"r"):
        in_queue.put(i) 

for i in range(THREAD_COUNT):
    in_queue.put(None)      
    
for worker in worker_list:
    worker.join()  
# with 4        
#real	1m17.021s
#user	1m2.530s
#sys	0m5.300s
#with 1
#real	1m19.310s
#user	1m4.490s
#sys	0m5.410s
#with 8 
#real	1m13.971s
#user	1m1.020s
#sys	0m5.070s
