#!/usr/bin/python
from optparse import OptionParser
import subprocess
import os,sys

options,args = None, None
p = OptionParser()
p.add_option("-r","--remove",action="store_true",dest="remove",help="if -r then directories are removed")

if len(sys.argv) == 1:
    p.print_help()

try:
    options,args = p.parse_args()
except IndexError:
    p.print_help()

are_you_sure = "No"

cwd = os.getcwd()
for root,dirs,files in os.walk(cwd):
    for adir in dirs:
        subprocess.call(["ls" ,"-ltr",os.path.join(root,adir)])
        if options.remove:
                    if are_you_sure == "No":
                        are_you_sure = raw_input("Are you SURE(Yes/No):")
                    if are_you_sure == "Yes":
                        subprocess.call(["rm" , "-rf" ,os.path.join(root,adir)])
