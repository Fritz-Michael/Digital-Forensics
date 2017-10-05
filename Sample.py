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
	x = 0
	signatures = findSignatures('\\\\.\\E:', 'E', 40000, 1000000, headers[0], footers[0] )
	for signature in signatures:
		recoverfile('\\\\.\\E:',signature[0],signature[1],x)
		x += 1
	