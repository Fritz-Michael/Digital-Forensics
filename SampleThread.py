import string
import time
import os
import platform
import operator
from thread import threading
try:
	from ctypes import windll
	import ctypes
	from WindowsFunctions import *
	print("hello")
except BaseException as e:
	from LinuxFunctions import *
	print(e)

if __name__ == '__main__':
