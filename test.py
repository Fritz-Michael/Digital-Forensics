import string
import time
import os
import platform
import operator
import threading
import binascii
from ctypes import windll
import ctypes

import multiprocessing
from multiprocessing import Manager

def gettotalsectors(path):
	drive = open(path,'rb')
	drive.read(40)
	sectors = int.from_bytes(drive.read(8), byteorder='little')
	drive.close()
	return sectors

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

def mftlocation(path, rootPath):
	drive = open(path,'rb')
	drive.read(48)
	location = int.from_bytes(drive.read(8),byteorder='little')
	location *= getsectorspercluster(rootPath)
	drive.close()
	return location

def getmetadata(path):
	#drive = open(path, 'rb')
	# print(path)
	# print(type(path))
	# print(type(drive))
	#drive.close()

	# metadata = [] # list of tuple/list
	
	currloc = mftlocation(path, 'H')
	print(currloc)
	print(type(currloc))
	
	#temploc = currloc
	drive = open(path, 'rb')
	drive.seek(currloc)
	fbyte = binascii.hexlify(drive.read(1))
	print(fbyte)
	drive.close()

	# #for mftrecordentry in mftrecords:
	# 	# drive.seek(currloc)
	# 	# fbyte = binascii.hexlify(drive.read(1))
	# 	# if fbyte == 'F':
	# 	# 	drive.seek(-1, 1)

	# 	# 	mac times
	# 	# 	getmac()
	# 	# 	metadata.append()

	# 	# 	mac filename
	# 	# 	getfilename()
	# 	# 	metadata.append()
	# 		currloc = drive.seek(currloc + 1024)
	# 		temploc = currloc
	# 	# else:
	# 	# 	drive.close()
	# 	# 	break


	
	#kapag ng open ng drive yung file pointer nandun pa rin kahit tapos na sa function at pwede pang gamitin sa ibang function basta hindi pa na close?

if __name__ == '__main__':
	getmetadata('\\\\.\\H:')


	#rootpath ==> path letter
	#additional ???
	#locHolder.append((posHeader,posFooter+additional)) tuple ba ito???
