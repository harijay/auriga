import sys,os
from process_multi_util_functions import safe_write_script

class ScalePackToMtzRunscriptCreator(object):
    """Class that accepts filename, (optional) spacegroup,cell_dimensions, wavelength and number of residues in the ASU as imput. Runs truncate and outputs the mtz file.
    """
    
    def __init__(self,filename,auriga_output_directory_root,spag=None,cell_dimensions_tuple=None,wavelength=None,number_of_residues_in_asu=130):
        """Assume only filename and infer cell dimensions and spacegroup
        """
        self.filename = filename.strip()
        self.file = open(self.filename.strip(),"r")
        self.spag = self.extract_spag()
        self.cell_dimensions_string = self.extract_cell_dimensions_string()
        self.wavelength = wavelength
        self.number_of_residues_in_asu = number_of_residues_in_asu
        self.title = os.path.splitext(os.path.split(self.filename)[1])[0] + "_autoproc"
        self.proj_name =  os.path.splitext(os.path.split(self.filename)[1])[0].upper()
        self.auriga_output_directory_root = auriga_output_directory_root
        self.scalepack2mtz_dict = dict(title = self.title ,spag = self.spag , cell = self.cell_dimensions_string , wavelength = self.wavelength , proj_name = self.proj_name)
        self.outputdir = os.path.join(self.auriga_output_directory_root,self.proj_name) 
        if not os.path.exists(self.outputdir):
            os.mkdir(self.outputdir)
            
    def extract_cell_dimensions_string(self):
        """
        Arguments:
        - `self`:
        """
        self.file.seek(0)
        self.file.readline()
        self.file.readline()
        cell_dimensions_string = ",".join(self.file.readline().split()[:-1])
       # print "CELL DIM STR" , cell_dimensions_string
        return cell_dimensions_string
    
    def extract_spag(self):
        self.file.seek(0)
        self.file.readline()
        self.file.readline()
        cell_line =  self.file.readline().split()
     #   print "CELL LINE" , cell_line
        return cell_line[-1]
    
    def describe(self):
        description = """Scalepack file:{self.filename},{self.spag},{self.cell_dimensions_string}""".format(self=self)
       # print description
        
    def mtzoutpath(self):
        return  os.path.join(self.outputdir,"{self.proj_name}_trnfreeR.mtz".format(self=self))
    
    def create_and_return_runscript_file(self):
        scrfile1 = open(os.path.join(self.outputdir,"%s_1.sh" % self.proj_name),"w")
        outfile_prefix  = os.path.join(self.outputdir,self.proj_name)
        # scrfile2 = open(os.path.join(self.outputdir,"%s_2.sh" % self.proj_name),"w")
        # scrfile3 = open(os.path.join(self.outputdir,"%s_3.sh" % self.proj_name),"w")
        # scrfile4 = open(os.path.join(self.outputdir,"%s_4.sh" % self.proj_name),"w")
    
      #  print "PROJ_NAME_OUTPREFIX set to ", outfile_prefix ,"DIRECTORY"
        
        scr1 =  """#!/bin/sh 
#set -e
# bug # 3192 - run-all examples produce harvest files - well to counteract
# this here set HARVESTHOME to somewhere in $CCP4_SCR

#HARVESTHOME=${self.outputdir}
#export HARVESTHOME

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
scalepack2mtz hklin {self.filename}  hklout {outfile_prefix}_junk1.mtz <<eof
name project {self.proj_name} crystal {self.proj_name} dataset {self.proj_name}
symm {self.spag}
end
eof

# convert Is to Fs and Ds.

truncate hklin {outfile_prefix}_junk1.mtz hklout {outfile_prefix}_junk2.mtz <<eof
title {self.proj_name} data 
truncate yes
nresidue {self.number_of_residues_in_asu}
labout  F=FP_{self.proj_name} SIGF=SIGFP_{self.proj_name}
end
eof

# get correct sort order and asymmetric unit

cad hklin1 {outfile_prefix}_junk2.mtz hklout {outfile_prefix}_trn.mtz <<eof
labi file 1 ALL
sort H K L
end
eof

# Add free r to reflections
freerflag hklin  {outfile_prefix}_trn.mtz hklout  {outfile_prefix}_trnfreeR.mtz <<eof
FREERFRAC 0.05
END
eof""".format(self=self, outfile_prefix = outfile_prefix)
        safe_write_script(scr1,scrfile1)
        return scrfile1.name
