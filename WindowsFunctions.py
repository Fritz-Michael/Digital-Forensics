import string
import time
import os
import platform
import operator
import threading
import binascii
from ctypes import windll
import ctypes
from WindowsFunctions import *
import multiprocessing

#### GLOBAL VARIABLES ####
headerSign = []
footerSign = []
extensionSign = []
locations = []

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
	#signaturesH = []
	#headers = open('headers.txt','r')
	with open('headers.txt') as openfileobject:
		for line in openfileobject:
			temp = []
			tempLine = line.split()
			for li in tempLine:
				temp.append(bytes(li,'utf-8'))
			#signaturesH.append(temp)
			headerSign.append(temp)
	#headers.close()
	#return signaturesH

def getFooters():
	#signaturesF = []
	temp = []
	#footers = open('footers.txt','r')
	with open('footers.txt') as openfileobject:
		for line in openfileobject:
			tempLine = line.split()
			for li in tempLine:
				temp.append(bytes(li,'utf-8'))
			#signaturesF.append(temp)
			footerSign.append(temp)
	#footers.close()
	#return signaturesF

def getExtensions():
	#extensions = []
	#ext = open('extensions.txt', 'r')
	with open('extensions.txt', 'r') as openfileobject:
		for line in openfileobject:
			#extensions.append(line)
			extensionSign.append(line)
	#ext.close()
	#return extensions

def findSignatures(path, rootPath, startSector, endSector, headers, footers, locHolder):
	time.sleep(0.2)
	bytesPerSector = getbytespersector(rootPath)
	sectorPerCluster = getsectorspercluster(rootPath)
	drive = open(path,'rb')
	cur = b'0'
	posHeader = 0
	posFooter = 0
	while startSector < endSector:
		drive.seek(int(bytesPerSector*startSector))
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
			locHolder.append((posHeader,posFooter))
	print("Im done", threading.current_thread().name)
	drive.close()

#thread function
def recoverfile(path, filepositions, extension):
	time.sleep(0.02)
	drive = open(path, 'rb')
	for fileposition in filepositions:
		start = fileposition[0]
		end = fileposition[1]
		image = open("found\\" + str(start) + extension,"wb")
		drive.seek(start-1)
		while start < end:
			cur = drive.read(1)
			image.write(cur)
			start += 1
		image.close()
		print("Saved ", extension, " file!")

if __name__ == '__main__':

	process = []
	start = time.time()

	### get the file types ###
	getHeaders()
	getFooters()
	getExtensions()
	##########################

	### searching for signatures ###
	for x in range(len(headerSign)):
		locations.append([])

	for x in range(len(headerSign)):
		process.append(multiprocessing.Process(target=findSignatures,args=('\\\\.\\E:','E',0,3000000,headerSign[x],footerSign[x],locations[x])))

	for x in range(len(headerSign)):
		process[x].start()

	for x in range(len(headerSign)):
		process[x].join()
	###############################

	process = []
	startRecover = time.time()
	### recovering files ###
	for x in range(len(headerSign)):
		process.append(multiprocessing.Process(target=recoverfile,args=('\\\\.\\E:',locations[x],extensionSign[x].rstrip())))

	for x in range(len(headerSign)):
		process[x].start()

	for x in range(len(headerSign)):
		process[x].join()
	########################

	print("total recover time: ", time.time()-startRecover)

	print("total time: ", time.time()-start)