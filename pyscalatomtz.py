#!/usr/bin/python
# Class that takes in a file name and other optional inputs and converts the scafile to an mtz file
from optparse import OptionParser
import aurigaerrors
import os
import sys
from  project_settings import auriga_proj_dir
import subprocess

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
        

    def run(self):
        scrfile = open(os.path.join(self.auriga_proj_dir,"%s.sh" % self.proj_name),"w")
        scr = """#!/bin/sh
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

scalepack2mtz hklin {self.filename}  hklout $CCP4_SCR/junk1.mtz <<eof
name project {self.proj_name} crystal {self.proj_name} dataset {self.proj_name}
symm {self.spag}
end
eof

# convert Is to Fs and Ds.

truncate hklin $CCP4_SCR/junk1.mtz hklout $CCP4_SCR/junk2.mtz <<eof
title {self.proj_name} red aucn2 data 
truncate yes
nresidue {self.number_of_residues_in_asu}
labout  F=FP_{self.proj_name} SIGF=SIGFP_self.proj_name
end
eof

# get correct sort order and asymmetric unit

cad hklin1 $CCP4_SCR/junk2.mtz hklout $CCP4_SCR/{self.proj_name}_trn.mtz <<eof
labi file 1 ALL
sort H K L
end
eof
#""".format(self = self)
        scrfile.write(scr)
        scrfile.close()
        os.chmod(scrfile.name,0755)
        print scrfile.name
        subprocess.call([scrfile.name])

if __name__ == '__main__':
    sca_listfile  = "scafiles.txt"
    for i in open(sca_listfile,"r"):
        print "I have", i
        myfile = scalatomtz(i)
        myfile.run()
        myfile.describe()
        
    
        
        
