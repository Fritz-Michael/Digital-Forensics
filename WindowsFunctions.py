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
	image = open("found\\" + str(filename) + ".jpg","wb")
	while startSector < endSector:
		cur = drive.read(1)
		image.write(cur)
		startSector += 1
	image.close()
	print("Saved!")

# def readdriveWin(path, rootPath):
# 	drive = open(path, 'rb')
# 	bytesPerSector = getbytespersector(rootPath)
# 	sectorPerCluster = getsectorspercluster(rootPath)
# 	sectorNo = 0
# 	sectorMax = 1000000000000
# 	prev = '0'
# 	cur = '0'
# 	imagectr = 0
# 	maxSize = 10000000
# 	printB = False 
# 	while sectorNo < sectorMax:
# 		cur = data = binascii.hexlify(drive.read(1))
# 		if prev == b'46' and cur == b'49':
# 			nextbyte = drive.read(1)
# 			if nextbyte == b'4c':
# 				nextbyte = drive.read(1)
# 				if nextbyte == b'45':
# 					print("Found!")
# 		prev = cur 
# 		sectorNo += 1

	# while sectorNo < sectorMax:
	# 	try:
	# 		drive.seek(sectorNo * bytesPerSector) # iterates per sector
	# 		cur = reader = drive.read(1) # reads the first byte of each sector
	# 		print(cur)
	# 		if cur == b'\xFF':
	# 			nextbyte = drive.read(1) # reads the second byte of each sector
	# 			print(nextbyte)
	# 			if nextbyte == b'\xD8': # will be true if a JPG file header, FFD8, is detected
	# 				print("FOUND - ", sectorNo)
	# 				imagectr += 1 # iterate to designate the image number
	# 				image = open("found\\" + str(imagectr) + ".jpg","wb") # creates a new file in the 'found' folder and allows to write in bytes
	# 				running = True # used to designate that the writer is running
	# 				image.write(b'\xFF') # writes the JPG headers to the new file
	# 				image.write(b'\xD8')
	# 				mCtr = 0 # mCtr is used as a limiter just in case the new file is not really a JPG file, it stops at 10Mb, can be removed if image files is larger
	# 				while running and mCtr < maxSize: # loops until the footer FFD9 is detected or arbitrary limit is reached
	# 					cur = reader = drive.read(1) # reads one byte at a time from the possible JPG file
	# 					print(cur)
	# 					image.write(cur) # write the byte from the JPG file read
	# 					if cur == b'\xD9' and prev == b'\xFF': # responsible for checking if the footer FFD9 is found
	# 						running = False # once the footer is found, running will be set to false to end the loop
	# 						image.close() # the file would be closed to save the image
	# 						print("Image Saved")
	# 						raw_input("pause")
	# 					prev = cur # sets the cur value to prev, this is used to detect the 2 bytes for FF and D9
	# 					mCtr += 1 # this counter is used to iterate until it reaches the arbitrary limit

	# 			if mCtr >= maxSize: # just in case the arbitrary value is reached, it would safely close the image
	# 				image.close()
	# 				print("Image Saved - failed")
	# 	except:
	# 		pass
	# 	sectorNo += 1
