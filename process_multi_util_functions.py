from threading import Lock
import os
import sys

mutex= Lock()

def report(message):
     mutex.acquire()
   #  print message
     sys.stdout.flush()
     mutex.release()

def safe_write_script(string,filehandle):
    mutex.acquire()
    filehandle.write(string)
    filehandle.close()
    os.chmod(filehandle.name,0o755)
    mutex.release()
