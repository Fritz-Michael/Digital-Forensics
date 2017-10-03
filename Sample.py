import string
import time
import os
import binascii
#from WindowsFunctions import *

if __name__ == '__main__':
	drive = open('headers.txt','r')
	print(drive.readline())
	print(drive.readline())
	drive.seek(0, 0)
	print(drive.readline())
