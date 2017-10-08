import string
import time
import os
import platform
import operator
import threading
import binascii
from queue import Queue
from ctypes import windll
import ctypes
from WindowsFunctions import *

print_lock = threading.Lock()
temp = []

def get_drivesWin():
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

def getHeaders():
	signaturesH = []
	temp = []
	headers = open('headers.txt','r')
	with open('headers.txt') as openfileobject:
		for line in openfileobject:
			tempLine = line.split()
			for li in tempLine:
				temp.append(li)
			signaturesH.append(temp)
	headers.close()
	return signaturesH

def getFooters():
	signaturesF = []
	temp = []
	footers = open('footers.txt','r')
	with open('footers.txt') as openfileobject:
		for line in openfileobject:
			tempLine = line.split()
			for li in tempLine:
				temp.append(li)
			signaturesF.append(temp)
	footers.close()
	return signaturesF

def getExtensions():
	extensions = []
	ext = open('extensions.txt', 'r')
	with open('extensions.txt', 'r') as openfileobject:
		for line in openfileobject:
			extensions.append(line)
	ext.close()
	return extensions

#thread function
def findSignatures(path, rootPath, startSector, endSector, headers, footers, extension):
	time.sleep(0.2)
	with print_lock:
		locations = []
		bytesPerSector = getbytespersector(rootPath)
		sectorPerCluster = getsectorspercluster(rootPath)
		drive = open(path,'rb')
		cur = b'0'
		posHeader = 0
		posFooter = 0
		head = ""
		foot = ""
		for header in headers:
			head += header
		for footer in footers:
			foot += footer 
		head = bytes(head,'utf-8')
		foot = bytes(foot,'utf-8')
		while startSector < endSector:
			drive.seek(bytesPerSector*startSector)
			foundHeader = False
			foundFooter = False
			cur = binascii.hexlify(drive.read(1))

			if cur == bytes(headers[0],'utf-8'):
				posHeader = drive.tell()
				nextbyte = binascii.hexlify(bytes(drive.read(8))) 
				if head == nextbyte:
					print("hello")
					foundHeader = True
				else:
					foundHeader = False
					drive.seek(posHeader)

				if foundHeader:
					while not foundFooter:
						cur = nextbyte = binascii.hexlify(drive.read(1))
						if nextbyte == footers[0]:
							if foot == binascii.hexlify(bytes(drive.read(8))):
								foundFooter = True
					posFooter = drive.tell()
			startSector += 1
			if foundHeader and foundFooter:
				recoverfile(path,posHeader,posFooter,posHeader-1,extension)
		print("Im done", threading.current_thread().name)

#thread function
def recoverfile(path, startSector, endSector,filename,extension):
	drive = open(path, 'rb')
	drive.read(startSector-1)
	print(drive.tell())
	image = open("found\\" + str(filename) + extension,"wb")
	while startSector < endSector:
		cur = drive.read(1)
		image.write(cur)
		startSector += 1
	image.close()
	print("Saved!")

sectors = 2097152
threadNo = 100
start = time.time()
headers = getHeaders()
footers = getFooters()
extensions = getExtensions()
z = int(sectors/threadNo)
for x in range(0,threadNo):
	t1 = threading.Thread(target=findSignatures, args=('\\\\.\\E:','E',z*x,z*(x+1)-1,headers[0],footers[0],extensions[0]))
	t2 = threading.Thread(target=findSignatures, args=('\\\\.\\E:','E',z*(x+1),z*(x+2)-1,headers[0],footers[0],extensions[0]))
	t3 = threading.Thread(target=findSignatures, args=('\\\\.\\E:','E',z*(x+2),z*(x+3)-1,headers[0],footers[0],extensions[0]))
	t4 = threading.Thread(target=findSignatures, args=('\\\\.\\E:','E',z*(x+3),z*(x+4)-1,headers[0],footers[0],extensions[0]))
	t1.daemon = True
	t2.daemon = True
	t3.daemon = True
	t4.daemon = True
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	z += z


for x in range(0,threadNo):
	t1.join()
	t2.join()
	t3.join()
	t4.join()

print("total time: ", time.time()-start)