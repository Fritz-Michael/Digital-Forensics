import string
from ctypes import windll
import time
import os

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives


if __name__ == '__main__':
	drives = set(get_drives())
	x = 0
	for drive in drives:
		print("[%d] %s" % (x,drive))
		x += 1
	