import io
import os
from filerecoveryfunctions import *
from ctypes import *


def format_drive_to_NTFS(path):
	format_drive(path,'NTFS','Drive')


def format_drive_to_FAT32(path):
	format_drive(path,'FAT32','Drive')


def format_drive_to_exFAT(path):
	format_drive(path,'exFAT','Drive')


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
	
