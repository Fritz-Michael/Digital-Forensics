import io
import os
from filerecoveryfunctions import *
from ctypes import *

def get_boot_sector_NTFS(path):
	drive = open(path,'rb')
	boot_sector = drive.read(512)
	drive.close()
	return boot_sector

def zero_drive(path,bytesPerSector,totalSectors):
	x = 0
	try:
		with open(path,'r+') as of:
			for x in range(totalSectors):
				of.write('\0' * bytesPerSector)
				of.flush()
				x += 1
				print(x)
	except OSError:
		pass

def write_boot_sector_NTFS(path):
	drive = open(path,'rb+')
	file = open('NTFS.txt','rb')
	boot_sector = file.read()
	drive.write(boot_sector)
	file.close()
	drive.close()

def format_drive_to_NTFS(path):
	format_drive(path,'NTFS','USBDrive')

def format_drive_to_FAT32(path):
	format_drive(path,'FAT32','USBDrive')

def format_drive_to_exFAT(path):
	format_drive(path,'exFAT','USBDrive')

def myFmtCallback(command, modifier, arg):
    print(command)
    return 1    # TRUE

def format_drive(Drive, Format, Title):
    api = windll.LoadLibrary('fmifs.dll')
    callback_function = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
    harddisk = 0x0C
    drive_type = 0
    api.FormatEx(c_wchar_p(Drive), drive_type, c_wchar_p(Format),
                c_wchar_p(Title), True, c_int(0), callback_function(myFmtCallback))


if __name__ == '__main__':
	format_drive_to_FAT32('E:\\')
	
