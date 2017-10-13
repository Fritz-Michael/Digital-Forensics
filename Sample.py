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
	

	print(binascii.unhexlify(headers[0]))