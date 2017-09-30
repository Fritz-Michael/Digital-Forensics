import string
import time
import os
import operator

def get_drivesLinux():
	dfoutput = [s.split() for s in os.popen("df -h | grep \"/media/root/\"").read().splitlines()]
	return dfoutput

def getblocksize(path):
	driveinfo = os.statvfs(path)
	return driveinfo.f_frsize

def getnumberofblocks(path):
	driveinfo = os.statvfs(path)
	return driveinfo.f_blocks

def getinodenumber(path):
	return os.stat(path).st_ino

def readdriveLinux(path):
	drivepath = open(path, 'rb')
	bytesPerSector = getblocksize(path)
	sectorPerCluster = getnumberofblocks(path)
	print(drivepath.read(1))

