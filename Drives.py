import string
import time
import os
from ctypes import windll
import ctypes
import platform
try:
	from WindowsFunctions import *
except BaseException:
	from LinuxFunctions import *

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

def getmetadata(path):
    return os.stat(path)

if __name__ == '__main__':
	dictDrive = []
	drives = set(get_drives())
	x = 0
	for drive in drives:
		print("[%d] %s" % (x,drive))
		x += 1
		dictDrive.append(drive)
	option = input("Choose a Drive: ")
	path = dictDrive[int(option)]
	temppath = '\\\\.\\' + path + ':'
	if platform.system() == 'Windows':
		readdriveWin(temppath, path)
	else:
		readdriveLinux(temppath, path)
		
        


        
        
