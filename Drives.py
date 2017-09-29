import string
from ctypes import windll
import ctypes
import time
import os
from dd import *

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

def getbytespersector(path):
	sectorsPerCluster = ctypes.c_ulonglong(0)
	bytesPerSector = ctypes.c_ulonglong(0)
	rootPathName = ctypes.c_wchar_p(u"" + path + ":\\")

	ctypes.windll.kernel32.GetDiskFreeSpaceW(rootPathName,
		ctypes.pointer(sectorsPerCluster),
		ctypes.pointer(bytesPerSector),
		None,
		None,
	)
	return bytesPerSector.value

def getsectorspercluster(path):
	sectorsPerCluster = ctypes.c_ulonglong(0)
	bytesPerSector = ctypes.c_ulonglong(0)
	rootPathName = ctypes.c_wchar_p(u"" + path + ":\\")

	ctypes.windll.kernel32.GetDiskFreeSpaceW(rootPathName,
		ctypes.pointer(sectorsPerCluster),
		ctypes.pointer(bytesPerSector),
		None,
		None,
	)
	return sectorsPerCluster.value

def readdrive(path, rootPath):
    drivepath = open(path, 'rb')
    bytesPerSector = getbytespersector(rootPath)
    sectorPerCluster = getsectorspercluster(rootPath)

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
	readdrive(temppath, path)
		
        


        
        
