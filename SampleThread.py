import string
import time
import os
import platform
import operator
import threading
from queue import Queue
from ctypes import windll
import ctypes
from WindowsFunctions import *

print_lock = threading.Lock()
temp = []

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

def getExtensions():
	extensions = []
	ext = open('extensions.txt', 'r')
	with open('extensions.txt', 'r') as openfileobject:
		for line in openfileobject:
			extensions.append(line)
	ext.close()
	return extensions

#thread function
def findSignatures(worker, path, rootPath, startSector, endSector, headers, footers, extension):
	time.sleep(0.5)
	with print_lock:
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

def threaderSignature(path, rootPath, startSector, endSector, headers, footers, extension):
	while True:
		worker = q.get()
		a = findSignatures(worker, path, rootPath, startSector, endSector, headers, footers, extension)
		q.task_done()
	return a 

def threaderRecover(path, startSector, endSector,filename,extension):
	while True:
		worker = q.get()
		recoverfile(worker, path, startSector, endSector,filename,extension)
		q.task_done() 

q = Queue()
y = 0
sectors = 3000000
threadNo = 200
headers = getHeaders()
footers = getFooters()
extensions = getExtensions()
for x in range(0,threadNo):
	t = threading.Thread(target=threaderSignature, args=('\\\\.\\E:','E',y,int(sectors/threadNo*(x+1)-1),headers[0],footers[0],extensions[0]))
	y += int(sectors/threadNo)
	t.daemon = True 
	t.start()

start = time.time()

for worker in range(threadNo):
	q.put(worker)
q.join()

print("total time: ", time.time()-start)