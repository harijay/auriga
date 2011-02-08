#!/usr/bin/env python
# -*- coding: latin-1 -*-

from  process_multi_util_functions import safe_write_script
import sys,os

class Refmac5RunScriptCreator(object):

    def __init__(self,phaseroutput_root,auriga_output_directory_root):
        self.mtzfile = phaseroutput_root.strip() + ".1.mtz"
        self.pdbfile = phaseroutput_root.strip() + ".1.pdb"
        self.phaseroutput_root = phaseroutput_root.strip()
        self.proj_name = os.path.split(phaseroutput_root)[-1]
        self.auriga_output_directory_root = auriga_output_directory_root
        self.outputdir = os.path.join(self.auriga_output_directory_root,self.proj_name)
        if os.path.exists(self.mtzfile) and os.path.exists(self.pdbfile):
            pass
        else:
            pass
       
    def write_runscript_and_return_name(self):
        self.comstring = """#!/bin/csh
#
#   Example of refinement by refmac
#
set inmtz={self.outputdir}/{self.proj_name}_trnfreeR.mtz
start:

set name = {self.proj_name}
set last = 1
set cycles = 1
set count = 0
while ($count != $cycles)
echo '*******************************************************************'
echo  $count
echo '*******************************************************************'
@ curr = $last + 1

#
# Refmac 
#
refmac:
refmac5 \
HKLIN   $inmtz \
HKLOUT   {self.outputdir}/{self.proj_name}.${{curr}}.mtz \
XYZIN   {self.outputdir}/{self.proj_name}.${{last}}.pdb \
XYZOUT  {self.outputdir}/{self.proj_name}.${{curr}}.pdb \
<< eor
#
#####Do not add hydrogens
#
MAKE_restraints HYDRogens No
#
#####Do not check correctness of all monomers. Rely on users naming
#####One should be careful in using this option.
#
MAKE CHECk 0
#
####Input mtz labels. 
#
LABIN FP=FP_{self.proj_name} SIGFP=SIGFP_{self.proj_name} FREE=FreeR_flag
#
####Output mtz labels
#
LABO FC=FC PHIC=PHIC    FWT=2FOFCWT PHWT=PH2FOFCWT -
                     DELFWT=FOFCWT  PHDELWT=PHFOFCWT
#
####Restrained refinement. Reflections between 20 1.5Å resolution will be used
#
REFI TYPE RESTrained RESOLUTION  20 1.10
#
####Use maximum likelihood residual
####Use maximum likelihood residual
#
REFI RESI MLKF
#
####Refine isotropic B values.
# 
REFI BREF ISOTropic  
#
####Use 0.35 as weighting between X-ray and geometry
# 
WEIGHT AUTO
#
####Scaling parameters. Use BULK solvent based on Babinet's principle.
####NB: Unless otherwise SOLVENT NO given contribution of bulk solvent
####based on constant value will be used. 
#
SCALe TYPE BULK   
#
####Fix Babinet's bulk solvent B value to 200.0
#
SCALe LSSCale FIXBulk 200.0
#
####number of refinement cycles
#
NCYC 2
#
####Monitor only overall statistics
# 
MONI MEDIUM
end
eor
if ($status) exit
#
@ last++
@ count++
end
""".format(self=self)
        self.mycomfile = open(os.path.join(self.outputdir,self.proj_name + "_refmac5_input.sh"),"w")
        safe_write_script(self.comstring,self.mycomfile)
        return self.mycomfile.name
