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
from multiprocessing import Manager

#### GLOBAL VARIABLES ####
headerSign = []
footerSign = []
extensionSign = []

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
	with open('headers.txt') as openfileobject:
		for line in openfileobject:
			temp = []
			tempLine = line.split()
			for li in tempLine:
				temp.append(bytes(li,'utf-8'))
			#signaturesH.append(temp)
			headerSign.append(temp)

def getFooters():
	with open('footers.txt') as openfileobject:
		for line in openfileobject:
			temp = []
			tempLine = line.split()
			for li in tempLine:
				temp.append(bytes(li,'utf-8'))
			footerSign.append(temp)

def getExtensions():
	with open('extensions.txt', 'r') as openfileobject:
		for line in openfileobject:
			extensionSign.append(line)

def findSignatures(path, rootPath, startSector, endSector, headers, footers, locHolder, additional):
	time.sleep(0.02)
	bytesPerSector = getbytespersector(rootPath)
	sectorPerCluster = getsectorspercluster(rootPath)
	drive = open(path,'rb')
	cur = b'0'
	posHeader = 0
	posFooter = 0
	maxsize = 1000000
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
				size = 0
				while not foundFooter and size != maxsize:
					cur = nextbyte = binascii.hexlify(drive.read(1))
					if nextbyte == footers[0]:
						for footer in footers:
							if footer == cur:
								cur = binascii.hexlify(drive.read(1))
								foundFooter = True
							else:
								foundFooter = False
								break
					size += 1
				posFooter = drive.tell()
		startSector += 1
		if foundHeader and foundFooter:
			print("huli ka", posHeader, posFooter)
			locHolder.append((posHeader,posFooter+additional))
	print("Im done", threading.current_thread().name)
	drive.close()

#thread function
def recoverfile(path, filepositions, extension):
	time.sleep(0.02)
	drive = open(path, 'rb')
	for fileposition in filepositions:
		start = fileposition[0]
		end = fileposition[1]
		image = open('found\\' + str(fileposition[0]) + extension, 'wb')
		drive.seek(start-1)
		while start < end:
			cur = drive.read(1)
			image.write(cur)
			start += 1
		image.close()
		print("Saved ", extension, " file!")
	drive.close()

def recoverdocxxlsx(path, filepositions):
	time.sleep(0.2)
	drive = open(path, 'rb')
	isdocx = False
	isxlsx = False
	prev = ''
	for fileposition in filepositions:
		start = fileposition[0]
		end = fileposition[1]
		image = open('found\\' + str(fileposition[0]), 'wb')
		drive.seek(start-1)
		while start < end:
			curPos = drive.tell()
			cur = drive.read(1)

			if binascii.hexlify(cur) == b'77' and not isdocx:
				drive.seek(curPos)
				header = binascii.hexlify(drive.read(5))
				if header == b'776f72642f':
					isdocx = True
					drive.seek(curPos+1)
				else:
					drive.seek(curPos+1)

			if binascii.hexlify(cur) == b'78' and not isxlsx:
				drive.seek(curPos)
				header = binascii.hexlify(drive.read(3))
				if header == b'786c2f':
					isxlsx = True
					drive.seek(curPos+1)
				else:
					drive.seek(curPos+1)

			image.write(cur)
			start += 1
			prev = cur
		image.close()
		if isdocx:
			os.rename('found\\' + str(fileposition[0]), 'found\\' + str(fileposition[0]) + '.docx')
			print("Saved ", ".docx", " file!")
		if isxlsx:
			os.rename('found\\' + str(fileposition[0]), 'found\\' + str(fileposition[0]) + '.xlsx')
			print("Saved ", ".xlsx", " file!")

def main():
	threads = 0
	manager = Manager()
	process = []
	locations = manager.list()
	start = time.time()
	### get the file types ###
	getHeaders()
	getFooters()
	getExtensions()
	##########################
	
	### searching for signatures ###
	for x in range(len(headerSign)):
		locations.append(manager.list())

	for x in range(len(headerSign)):
		if extensionSign[x] == '.docx':
			process.append(threading.Thread(target=findSignatures,args=('\\\\.\\E:','E',0,3000000,headerSign[x],footerSign[x],locations[x],20)))
		else:
			process.append(threading.Thread(target=findSignatures,args=('\\\\.\\E:','E',0,3000000,headerSign[x],footerSign[x],locations[x],0)))

	for x in range(len(headerSign)):
		process[x].start()

	for x in range(len(headerSign)):
		process[x].join()
	###############################

	process = []
	startRecover = time.time()
	### recovering files ###
	for x in range(len(headerSign)):
		if extension[x] == '.docx':
			process.append(threading.Thread(target=recoverdocxxlsx,args=('\\\\.\\E:',locations[x])))
		else:
			process.append(threading.Thread(target=recoverfile,args=('\\\\.\\E:',locations[x],extensionSign[x].rstrip())))

	for x in range(len(headerSign)):
		process[x].start()

	for x in range(len(headerSign)):
		process[x].join()
	########################
	print("total recover time: ", time.time()-startRecover)

	print("total time: ", time.time()-start)

if __name__ == '__main__':
	pass