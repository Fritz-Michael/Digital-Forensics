import string
import time
import os
import binascii
from ctypes import windll
import ctypes
from psutil import *
from WindowsFunctions import *

if __name__ == '__main__':
	start = time.time()
	drive = open('\\\\.\\E:', 'rb')
	drive.read(1)
	drive.close()
	print("total time: ", time.time() - start)
