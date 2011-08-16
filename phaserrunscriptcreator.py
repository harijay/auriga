#!/usr/bin/env python
from mrdict import modeldict
from process_multi_util_functions import safe_write_script
import os,sys

class PhaserRunScriptCreator(object):
    """Class that runs automated molecular replacement using phaser
    """
    
    def __init__(self,inputmtzpath,auriga_output_directory_root):
        """Class looks at input mtz , gets the right pdb and number of molecules from mrdict.mrdict and then launches a phaser run
        """
        self.mycomfile = None
        self.outfilepath = None
        self.proj_name = None
        self.auriga_output_directory_root = auriga_output_directory_root
        try:
            self.data_tuple   = modeldict[os.path.splitext(os.path.split(inputmtzpath)[1])[0].split("_")[0].upper()]
            self.inputmtzpath = inputmtzpath
            self.pdb_path = self.data_tuple[0]
            self.num_copies = self.data_tuple[1]
            self.proj_name =  "_".join(os.path.splitext(os.path.split(self.inputmtzpath)[1])[0].split("_")[0:2]).upper()
            self.outfilepath = os.path.join(os.path.join(self.auriga_output_directory_root,self.proj_name),self.proj_name)
            self.mycomfile = """#!/bin/sh 
phaser <<eof
TITLE {self.proj_name} phaser run automatic
MODE MR_AUTO
HKLIn {self.inputmtzpath}
LABIn F=FP_{self.proj_name} SIGF=SIGFP_{self.proj_name}
ENSEmble 1    PDBfile {self.pdb_path} RMS 1.2
COMPosition PROTein MW 14200 NUM {self.num_copies} #beta
SEARch ENSEmble 1 NUM {self.num_copies}
PACK SELECT ALLOW
ROOT {self.outfilepath} # not the default
eof""".format(self=self)
        except KeyError:
            pass
        
    def write_runscript_and_return_name(self):
        comfile = open(os.path.join(os.path.join(self.auriga_output_directory_root,self.proj_name),self.proj_name  + "_phaser_input.sh"),"w")
        safe_write_script(self.mycomfile,comfile)
        return comfile.name
        
        
        
