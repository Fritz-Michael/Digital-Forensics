import string
import time
import os
from ctypes import windll
import ctypes

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

	a = ctypes.windll.kernel32.GetDiskFreeSpaceW(rootPathName,
		ctypes.pointer(sectorsPerCluster),
		ctypes.pointer(bytesPerSector),
		None,
		None,
	)
	print(a)
	return sectorsPerCluster.value

def readdriveWin(path, rootPath):
	drive = open(path, 'rb')
	bytesPerSector = getbytespersector(rootPath)
	sectorPerCluster = getsectorspercluster(rootPath)

	sectorNo = 0
	sectorMax = 10000000
	prev = '0'
	cur = '0'
	imagectr = 0
	maxSize = 10000000

	while sectorNo < sectorMax:
		try:
			drive.seek(sectorNo * bytesPerSector) # iterates per sector
			cur = reader = drive.read(1) # reads the first byte of each sector

			if cur == b'\xFD':
				nextbyte = drive.read(1) # reads the second byte of each sector
				if nextbyte == b'\xD8': # will be true if a JPG file header, FFD8, is detected
					print("FOUND - ", sectorNo)
					imagectr += 1 # iterate to designate the image number
					image = open("found\\" + str(imagectr) + ".jpg","wb") # creates a new file in the 'found' folder and allows to write in bytes
					print("hello")
					running = True # used to designate that the writer is running
					image.write(b'\xFF') # writes the JPG headers to the new file
					image.write(b'\xD8')
					mCtr = 0 # mCtr is used as a limiter just in case the new file is not really a JPG file, it stops at 10Mb, can be removed if image files is larger
					while running and mCtr < maxSize: # loops until the footer FFD9 is detected or arbitrary limit is reached
						cur = reader = drive.read(1) # reads one byte at a time from the possible JPG file
						image.write(cur) # write the byte from the JPG file read
						if cur == b'\xD9' and prev == b'\xFF': # responsible for checking if the footer FFD9 is found
							running = False # once the footer is found, running will be set to false to end the loop
							image.close() # the file would be closed to save the image
							print("Image Saved")
						prev = cur # sets the cur value to prev, this is used to detect the 2 bytes for FF and D9
						mCtr += 1 # this counter is used to iterate until it reaches the arbitrary limit

				if mCtr >= maxSize: # just in case the arbitrary value is reached, it would safely close the image
					image.close()
					print("Image Saved - failed")
		except:
			pass
		sectorNo += 1
