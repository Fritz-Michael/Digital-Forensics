import string
import time
import os
import binascii
from ctypes import windll
import ctypes
from psutil import *
from WindowsFunctions import *

if __name__ == '__main__':
	headers = getHeaders()
	footers = getFooters()
	extensions = getExtensions()
	x = 0
	string = ""
	for header in headers[0]:
		string += header
	drive = open('\\\\.\\E:', 'rb')
	drive.seek(1435967488)
	print(bytes(string,'utf-8') == binascii.hexlify(drive.read(8)))