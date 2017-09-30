import string
import time
import os
import platform
import operator
try:
	from ctypes import windll
	import ctypes
	from WindowsFunctions import *
except BaseException:
	from LinuxFunctions import *

def getmetadata(path):
    return os.stat(path)

if __name__ == '__main__':
	dictDrive = []

	if platform.system() == 'Windows':
		drives = set(get_drivesWin())
		x = 0
		for drive in drives:
			print("[%d] %s" % (x,drive))
			x += 1
			dictDrive.append(drive)
		option = input("Choose a Drive: ")
		path = dictDrive[int(option)]
		temppath = '\\\\.\\' + path + ':'
	else:
		drives = get_drivesLinux()
		x = 0
		for drive in drives:
			print("[%d] %s %s" % (x,drive[0],drive[-1]))
			x += 1
			dictDrive.append(drive[0])
		option = input("Choose a Drive: ")
		path = dictDrive[int(option)]

	if platform.system() == 'Windows':
		readdriveWin(temppath, path)
	else:
		readdriveLinux(path)
		
        


        
        
