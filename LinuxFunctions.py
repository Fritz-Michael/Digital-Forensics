import string
import time
import os

def getblocksize(path):
	driveinfo = os.statvfs(path)
	return driveinfo.F_FRSIZE

def getnumberofblocks(path):
	driveinfo = os.statvfs(path)
	return driveinfo.F_BLOCKS

def readdriveLinux(path, rootPath):
	drivepath = open(path, 'rb')
    bytesPerSector = getblocksize(rootPath)
    sectorPerCluster = getnumberofblocks(rootPath)
    print(drivepath.read(1))
