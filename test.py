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

def getMACtimes(path, rootPath, mft): 
	drive = open(path,'rb')
	drive.read(1)
	mft *= getbytespersector(rootPath)
	drive.seek(int(mft))
	drive.read(80)
	creation = binascii.hexlify(drive.read(8))
	modified = binascii.hexlify(drive.read(8))
	access = binascii.hexlify(drive.read(8))
	drive.close()
	return (creation,modified,access)

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
		# namesize = drive.read(1)
		# namesize = int.from_bytes(namesize,byteorder='little')
		# print(namesize)
		# print(offset)
		# filename = drive.read(namesize*2).decode('utf-16')
		# drive.close()
		# return filename

	else: #fnames below 32
		drive.seek(int(mft))
		offset = 240
		drive.read(offset)

	 #360 , 240 , 216/215 short files
	# x = 0
	# while x != 240:
	# 	print(drive.read(1), 'Byte loc: ', x)
	# 	x+=1
	# 	a=input('pause')

	namesize = drive.read(1)
	if int.from_bytes(namesize,byteorder='little') > 32 and nfile == False or int.from_bytes(namesize,byteorder='little') == 0 and nfile == False:

		offset = 216
		drive.seek(int(mft))
		drive.read(offset)
		namesize = drive.read(1)



	# if int.from_bytes(namesize,byteorder='little') == 12: #long filename offset 360

	# 	offset = 360
	# 	drive.seek(int(mft))
	# 	drive.read(offset)
	# 	namesize = drive.read(1)


	namesize = int.from_bytes(namesize,byteorder='little')

	# print(namesize)
	# print(offset)
	drive.read(1)
	filename = drive.read(namesize*2).decode('utf-16')

	if filename.find("~",0, namesize) == -1:
		drive.close()
		return filename
	# drive.read(1)
	# filename = drive.read(namesize*2).decode('utf-16')
	# drive.close()
	# return filename
	# if namesize <= 32 and namesize != 0:
	# 	drive.read(1)
	# 	filename = drive.read(namesize*2).decode('utf-16')
	# 	drive.close()
	# 	return filename
	else:
		# print('Index: ', filename.find("~",0, namesize))
		# print('burat found')
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
			fdate =
			if fname == None:
				ncount +=1
			if fname != None:
				fnameMeta.append(fname)
				# dateMeta.append(getMACtimes(path, rootpath, currsec))
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
	drive.close()


if __name__ == '__main__':
	getmetadata('\\\\.\\H:', 'H')



	#rootpath ==> path letter
	#additional ???
	#locHolder.append((posHeader,posFooter+additional)) tuple ba ito???