import string
import time
import os
import binascii
from ctypes import windll
import ctypes
from psutil import *
from WindowsFunctions import *
import multiprocessing
from multiprocessing import Manager
import threading

location = []
queues = []

def x(num,mult):
	num.append(mult)

if __name__ == '__main__':
	drive = open('\\\\.\\E:','rb')
	print(binascii.hexlify(drive.read(5)))
	drive.close()