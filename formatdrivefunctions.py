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

def myFmtCallback(command, modifier, arg):
    print(command)
    return 1    # TRUE

def format_drive(Drive, Format, Title):
    fm = windll.LoadLibrary('fmifs.dll')
    FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
    FMIFS_HARDDISK = 0x0C
    FMIFS_UNKNOWN = 0
    fm.FormatEx(c_wchar_p(Drive), FMIFS_UNKNOWN, c_wchar_p(Format),
                c_wchar_p(Title), True, c_int(0), FMT_CB_FUNC(myFmtCallback))


if __name__ == '__main__':
	format_drive_NTFS_to_FAT32('E:\\')
	
