import string
import time
import os
import binascii
from ctypes import windll
import ctypes
from psutil import *

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
				temp.append(bytes(li,'utf-8'))
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
				temp.append(bytes(li,'utf-8'))
			signaturesF.append(temp)
	footers.close()
	return signaturesF

#thread function
def findSignatures(path, rootPath, startSector, endSector, headers, footers):
	locations = []
	bytesPerSector = getbytespersector(rootPath)
	sectorPerCluster = getsectorspercluster(rootPath)
	drive = open(path,'rb')
	cur = b'0'
	posHeader = 0
	posFooter = 0
	while startSector < endSector:
		drive.seek(bytesPerSector*startSector)
		foundHeader = False
		foundFooter = False  
		cur = binascii.hexlify(drive.read(1))
		if cur == headers[0]:
			posHeader = drive.tell()
			nextbyte = cur 
			for header in headers:
				if header == nextbyte:
					nextbyte = binascii.hexlify(drive.read(1))
					foundHeader = True 
				else:
					drive.seek(posHeader, 0)
					foundHeader = False
					break
			if foundHeader:
				while not foundFooter:
					cur = nextbyte = binascii.hexlify(drive.read(1))
					if nextbyte == footers[0]:
						for footer in footers:
							if footer == cur:
								cur = binascii.hexlify(drive.read(1))
								foundFooter = True
							else:
								foundFooter = False
				posFooter = drive.tell()
		startSector += 1
		if foundHeader and foundFooter:
			locations.append((posHeader,posFooter))
	return locations


#thread function
def recoverfile(path, startSector, endSector,filename):
	drive = open(path, 'rb')
	drive.read(startSector-1)
	print(drive.tell())
	image = open("found\\" + str(filename) + ".png","wb")
	while startSector < endSector:
		cur = drive.read(1)
		image.write(cur)
		startSector += 1
	image.close()
	print("Saved!")
