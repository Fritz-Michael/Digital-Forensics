import string
import time
import os
import platform
import operator
import threading
import binascii
from ctypes import windll
import ctypes
import datetime
import multiprocessing
from multiprocessing import Manager
import struct

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

def getMACtimes(path, rootPath, mft): 
	drive = open(path,'rb')
	drive.read(1)
	mft *= getbytespersector(rootPath)
	drive.seek(int(mft))
	drive.read(80)
	create = drive.read(8)
	modified = drive.read(8)
	access = drive.read(8)
	drive.close()
	return (gettime(create),gettime(modified),gettime(access))

### converts filetime to datetime object
### PARAMETERS
	#filetime - bytes that represent the filetime
def gettime(filetime):
    Ftime = int(struct.unpack('<Q', filetime)[0])
    Epoch = divmod(Ftime - 116444736000000000, 10000000)
    Actualtime = datetime.datetime.fromtimestamp(Epoch[0])
    return Actualtime.strftime('%Y-%m-%d %H:%M:%S')

def getfilename(path, rootPath, mft):
	drive = open(path,'rb')
	drive.read(1)
	nfile = False
	mft *= getbytespersector(rootPath)
	drive.seek(int(mft))
	fbyte = drive.read(5).decode('utf-8')

	if fbyte == 'FILE*': #long filenames len == 40 >
		drive.seek(int(mft))
		offset = 232
		drive.read(offset)
		nfile = True

	else: #fnames below 32
		drive.seek(int(mft))
		offset = 240
		drive.read(offset)

	namesize = drive.read(1)

	if int.from_bytes(namesize,byteorder='little') > 32 and nfile == False or int.from_bytes(namesize,byteorder='little') == 0 and nfile == False:
		offset = 216
		drive.seek(int(mft))
		drive.read(offset)
		namesize = drive.read(1)

	namesize = int.from_bytes(namesize,byteorder='little')
	drive.read(1)
	filename = drive.read(namesize*2).decode('utf-16')

	if filename.find("~",0, namesize) == -1:
		drive.close()
		return filename
	else:
		if offset == 240 and namesize != 12: #folder directory offset 352
			offset = 352
			drive.seek(int(mft))
			drive.read(offset)
			namesize = drive.read(1)
			namesize = int.from_bytes(namesize,byteorder='little')
			drive.read(1)
			filename = drive.read(namesize*2).decode('utf-16')
			drive.close()
			return filename

		elif offset == 240 and namesize == 12:
			offset = 360
			drive.seek(int(mft))
			drive.read(offset)
			namesize = drive.read(1)
			namesize = int.from_bytes(namesize,byteorder='little')
			drive.read(1)
			filename = drive.read(namesize*2).decode('utf-16')
			drive.close()
			return filename

		drive.close()
		return None
	

def getmetadata(path, rootpath):
	drive = open(path, 'rb')
	currsec = mftlocation(path, rootpath)
	ncount = 0
	x = 0
	ifMFTtable = True
	fnameMeta = []
	dateMeta = []

	while ifMFTtable:
		currboff = getbytespersector(rootpath) * currsec
		drive.seek(currboff)
		fbyte = drive.read(4).decode('utf-8')

		if fbyte == 'FILE':
			print('Current Sector: ',currsec)
			
			fname = getfilename(path, rootpath, currsec)
			fdate = getMACtimes(path, rootpath, currsec)
			if fname == None:
				ncount +=1
			if fname != None:
				fnameMeta.append(fname)
				dateMeta.append(fdate)
			# print(x)

			x+=1
			# print(fname)
			currsec += 2
			# a = input('pause')
		elif fbyte == 'BAAD':
			currsec += 2
		else:
			ifMFTtable = False
		 	# break
	print('Number of MFT Entries: ',x)	
	print('Number of None: ', ncount)

	for num in fnameMeta:
		print(num)
	for wat in fdate:
		print(wat)
	drive.close()


if __name__ == '__main__':
	getmetadata('\\\\.\\H:', 'H')

