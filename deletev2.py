import string
import time
import os
import platform
import operator
import threading
import binascii
from ctypes import windll
import ctypes
import datetime
import multiprocessing
from multiprocessing import Manager
import struct
import random

def gettotalsectors(path):
    drive = open(path,'rb')
    drive.read(40)
    sectors = int.from_bytes(drive.read(8), byteorder='little')
    drive.close()
    return sectors

def getbytespersector(path):
    sectorsPerCluster = ctypes.c_ulonglong(0)
    bytesPerSector = ctypes.c_ulonglong(0)
    rootPathName = ctypes.c_wchar_p(u"" + path + ":\\")

    ctypes.windll.kernel32.GetDiskFreeSpaceW(rootPathName,
        ctypes.pointer(sectorsPerCluster),
        ctypes.pointer(bytesPerSector),
        None,
        None,
    )
    return bytesPerSector.value

def getsectorspercluster(path):
    sectorsPerCluster = ctypes.c_ulonglong(0)
    bytesPerSector = ctypes.c_ulonglong(0)
    rootPathName = ctypes.c_wchar_p(u"" + path + ":\\")

    ctypes.windll.kernel32.GetDiskFreeSpaceW(rootPathName,
        ctypes.pointer(sectorsPerCluster),
        ctypes.pointer(bytesPerSector),
        None,
        None,
    )
    return sectorsPerCluster.value

def mftlocation(path, rootPath):
    drive = open(path,'rb')
    drive.read(48)
    location = int.from_bytes(drive.read(8),byteorder='little')
    location *= getsectorspercluster(rootPath)
    drive.close()
    return location

def getdloc(offset, path, rootpath): # change rootpath later for byte position of MFT record 
    drive = open(path, 'rb')
    multidrun = False
    mdrun = []
    ### skip initial system entry ###
    ### getting position place in driver ###
    
    currboff = offset
    currMFTrec = currboff
    drive.seek(currboff)
    drive.read(20) ### read 20 ###
    nattroff = int.from_bytes(drive.read(2),byteorder='little') #next attribute from file header
    curattrhead = b'00000000'

    mftstatus = binascii.hexlify(drive.read(2))

    drive.seek(20, 1)

    recnum = int.from_bytes(drive.read(4),byteorder='little')

    if mftstatus == b'0000':
        drive.close()
        return None

    if mftstatus == b'0300':
        isfolder = True
    else:
        isfolder = False

    while curattrhead != b'30000000':
        drive.seek(currboff)
        drive.seek(nattroff, 1)
        currboff = drive.tell()
        curattrhead = binascii.hexlify(drive.read(4)) #atrib type
        nattroff = int.from_bytes(drive.read(4),byteorder='little') #attrib size

    drive.seek(16, 1)

    pdir = int.from_bytes(drive.read(6),byteorder='little')
    
    drive.seek(58, 1)
    fsize = int.from_bytes(drive.read(1),byteorder='little')

    drive.read(1)
    
    fname = drive.read(2 * fsize).decode('utf-16')

    if fname.find("~",0, fsize) != -1:
        drive.seek(currboff)
        drive.seek(natttroff, 1)
        currboff = drive.tell()
        curattrhead = binascii.hexlify(drive.read(4)) #atrib type
        nattroff = int.from_bytes(drive.read(4),byteorder='little') #attrib size
        drive.seek(16, 1)

        pdir = int.from_bytes(drive.read(6),byteorder='little')
        
        drive.seek(58, 1)
        fsize = int.from_bytes(drive.read(1),byteorder='little')

        drive.read(1)
        
        fname = drive.read(2 * fsize).decode('utf-16')
    
    if isfolder:
        drive.close()
        return {'is_folder': True, 'file_name': fname, 'parent_dir': pdir, 'MFT_rec': recnum}


    while curattrhead != b'80000000':
        drive.seek(currboff)
        drive.seek(nattroff, 1)
        currboff = drive.tell()
        curattrhead = binascii.hexlify(drive.read(4)) #atrib type
        nattroff = int.from_bytes(drive.read(4),byteorder='little') #attrib size
        nrflag = int.from_bytes(drive.read(1),byteorder='little') # nr or r
    
    drive.seek(currboff)
    if nrflag:
        drive.seek(32, 1) #offset to data run offset
        drunoff = int.from_bytes(drive.read(2),byteorder='little') #data run offset
        drive.seek(drunoff - 34, 1)
        dsize = binascii.hexlify(drive.read(1))
        high, low = int(dsize[:1], 16), int(dsize[1:2], 16)
        clustsize = int.from_bytes(drive.read(low),byteorder='little')* getsectorspercluster(rootpath) * getbytespersector(rootpath)
        drstart = int.from_bytes(drive.read(high),byteorder='little') * getsectorspercluster(rootpath) * getbytespersector(rootpath)
        
        if binascii.hexlify(drive.read(1)) == b'00':
            drive.close()
            return {'is_folder': False, 'file_name': fname, 'parent_dir': pdir, 'MFT_rec': recnum, 'multi_run': False, 'data_start': drstart, 'data_totalsize': clustsize}
            #delete(path, drstart, clustsize)
        else:
            drive.seek(-1, 1)
            mdrun.append((drstart, clustsize))
            while binascii.hexlify(drive.read(1)) != b'00':
                drive.seek(-1, 1)
                dsize = binascii.hexlify(drive.read(1))
                high, low = int(dsize[:1], 16), int(dsize[1:2], 16)
                clustsize = int.from_bytes(drive.read(low),byteorder='little')* getsectorspercluster(rootpath) * getbytespersector(rootpath)
                drstart = int.from_bytes(drive.read(high),byteorder='little') * getsectorspercluster(rootpath) * getbytespersector(rootpath)
                mdrun.append((drstart, clustsize))

            #delete(path, mdrun, multi=True)
            drive.close()
            return {'is_folder': False, 'file_name': fname, 'parent_dir': pdir, 'MFT_rec': recnum, 'multi_run': True, 'data_start': mdrun, 'data_totalsize': clustsize}
        # drive.seek(drstart)
        # call function for deletion - pass, byte position, clustersize/ data size, MFT entry position
        # return drstart, clustsize, currboff
    else:
        drive.seek(16, 1)
        dlen = int.from_bytes(drive.read(4),byteorder='little')
        doff = int.from_bytes(drive.read(2),byteorder='little')
        drive.seek(doff - 22, 1)
        
        drive.close()
        return {'is_folder': False, 'file_name': fname, 'parent_dir': pdir, 'MFT_rec': recnum, 'multi_run': False, 'data_start': drive.tell(), 'data_totalsize': dlen}
        # smdata = drive.read(dlen).decode('utf-8')
        delete(path, drive.tell(), dlen)
    updatestatus(currMFTrec)
    drive.close()
        # call fucntion for deletion - pass byte position, length of data, MFT entry position
    ### return start MFT file post, position of data blocks, number of clusters ###
    


def deletion(datarun, datasize, method, fpath,  npass=0):
    drive = open(fpath,'r+b')

    drive.seek(datarun)
    method = 0

    if method == 0:
        # zero fill
        for ctr in range(datasize):
            drive.write(struct.pack('s', b'\x00'))

    if method == 1:
        # secure wipe
        for ctr in range(datasize):
            # randomize
            dictio = ['00','11']
            rnd = random.choice(dictio)
            rnd = binascii.unhexlify(rnd)

            drive.write(struct.pack('s', rnd))      

    if method == 2:
        # schneier
        for outctr in range(7):
            if outctr == 0:
                for ctr in range(datasize):
                    drive.write(struct.pack('s', b'\x00'))
            elif outctr == 1:
                for ctr in range(datasize):
                    drive.write(struct.pack('s', b'\x11'))
            else:
                dictio = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
                for ctr in range(datasize):
                    character = random.choice(dictio)
                    character = character + random.choice(dictio)
                    character = binascii.unhexlify(character)
                    drive.write((struct.pack('s', character)))

    if method == 3:
      # random data
      dictio = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
      for outctr in range(npass):
          for ctr in range(datasize):
                character = random.choice(dictio)
                character = character + random.choice(dictio)
                character = binascii.unhexlify(character)
                drive.write((struct.pack('s', character)))

if __name__ == '__main__':
    # drive = open('\\\\.\\H:', 'rb')
    dirs = []

    currsec = mftlocation('\\\\.\\H:', 'H')
    currsec = 2097284
    currsec = 2097162
    currboff = currsec * getbytespersector('H')
    here = getdloc(currboff,'\\\\.\\H:', 'H')

    here["start_sector"] = currsec
    here["end_sector"] = currsec + 1

    if here["is_folder"]:
        rootpath = "H:"
        if here["MFT_rec"] == here["parent_dir"]:
            root = here["MFT_rec"]
            path = rootpath
        else:
            for directory in dirs:
                if directory["record_number"] == here["parent_dir"]:
                    path = directory["dir_path"] + "\\" + here["file_name"]
                    directory["num_child"] += 1
        
        dirs.append({'is_folder': here["is_folder"],'folder_name': here["file_name"], 'record_number': here["MFT_rec"], 'parent_directory': here["parent_dir"], 'dir_path': path, 'num_child': 0, 'list_child': []})



    else:
        for directory in dirs:
            if directory["record_number"] == here["parent_dir"]:
                here["dir_path"] = directory["dir_path"] + "\\" + here["file_name"]
                directory["num_child"] += 1
                directory["list_child"].append(here)



    print("Record Number:",here["MFT_rec"], "\n")
    print("Is Folder:",here["is_folder"], "\n")

    if here["is_folder"]:
        for x in dirs:
            if here["MFT_rec"] == x["record_number"]:
                print("Folder name:",x["folder_name"], "\n")
                print("Folder MFT record number:",x["record_number"], "\n")
                print("File path:",x["dir_path"], "\n")
                print("Number of files:", x["num_child"], "\n")
    print("File Name:",here["file_name"], "\n")
    print("Parent Directory:",here["parent_dir"], "\n")

    print("----------------------------------------\n")

    currsec = mftlocation('\\\\.\\H:', 'H')
    currsec = 2097282
    # currsec = 2097162
    currboff = currsec * getbytespersector('H')
    here = getdloc(currboff,'\\\\.\\H:', 'H')

    here["start_sector"] = currsec
    here["end_sector"] = currsec + 1

    if here["is_folder"]:
        rootpath = "H:"
        if here["MFT_rec"] == here["parent_dir"]:
            root = here["MFT_rec"]
            path = rootpath
        else:
            for directory in dirs:
                if directory["record_number"] == here["parent_dir"]:
                    path = directory["dir_path"] + "\\" + here["file_name"]
                    directory["num_child"] += 1
        
        dirs.append({'is_folder': here["is_folder"],'folder_name': here["file_name"], 'record_number': here["MFT_rec"], 'parent_directory': here["parent_dir"], 'dir_path': path, 'num_child': 0, 'list_child': []})



    else:
        for directory in dirs:
            if directory["record_number"] == here["parent_dir"]:
                here["dir_path"] = directory["dir_path"] + "\\" + here["file_name"]
                directory["num_child"] += 1
                directory["list_child"].append(here)



    print("Record Number:",here["MFT_rec"], "\n")
    print("Is Folder:",here["is_folder"], "\n")

    if here["is_folder"]:
        for x in dirs:
            if here["MFT_rec"] == x["record_number"]:
                print("Folder name:",x["folder_name"], "\n")
                print("Folder MFT record number:",x["record_number"], "\n")
                print("File path:",x["dir_path"], "\n")
                print("Number of files:", x["num_child"], "\n")
    print("File Name:",here["file_name"], "\n")
    print("Parent Directory:",here["parent_dir"], "\n")


    print("----------------------------------------\n")

    currsec = mftlocation('\\\\.\\H:', 'H')
    currsec = 2097284
    # currsec = 2097162
    # currsec = 2097322
    currboff = currsec * getbytespersector('H')
    here = getdloc(currboff,'\\\\.\\H:', 'H')

    here["start_sector"] = currsec
    here["end_sector"] = currsec + 1

    if here["is_folder"]:
        rootpath = "H:"
        if here["MFT_rec"] == here["parent_dir"]:
            root = here["MFT_rec"]
            path = rootpath
        else:
            for directory in dirs:
                if directory["record_number"] == here["parent_dir"]:
                    path = directory["dir_path"] + "\\" + here["file_name"]
                    directory["num_child"] += 1
        
        dirs.append({'is_folder': here["is_folder"],'folder_name': here["file_name"], 'record_number': here["MFT_rec"], 'parent_directory': here["parent_dir"], 'dir_path': path, 'num_child': 0, 'list_child': []})



    else:
        for directory in dirs:
            if directory["record_number"] == here["parent_dir"]:
                here["dir_path"] = directory["dir_path"] + "\\" + here["file_name"]
                directory["num_child"] += 1
                directory["list_child"].append(here)



    print("Record Number:",here["MFT_rec"], "\n")
    print("Is Folder:",here["is_folder"], "\n")

    if here["is_folder"]:
        for x in dirs:
            if here["MFT_rec"] == x["record_number"]:
                print("Folder name:",x["folder_name"], "\n")
                print("Folder MFT record number:",x["record_number"], "\n")
                print("File path:",x["dir_path"], "\n")
                print("Number of files:", x["num_child"], "\n")
    else:
        for x in dirs:
            for y in x["list_child"]:
                #child here
    print("File path:",here["dir_path"], "\n")
    print("File Name:",here["file_name"], "\n")
    print("Parent Directory:",here["parent_dir"], "\n")


    



























    #deletion part

    # for fold in dirs:
    #   if fold["record_number"] == here["parent_dir"]:
    #       here{'file_path': fold["dirpath"] + "\\" + here["file_name"]}

    # open(here["file_path"], 'r+b')


    # secure erase
    #   1 pass: one or zero (use random)
    # zero fill
    #   1 pass: zero only
    # schneier
    #   7 passes:
    #       Pass 1: Writes a one
    #       Pass 2: Writes a zero
    #       Pass 3: Writes a stream of random characters
    #       Pass 4: Writes a stream of random characters
    #       Pass 5: Writes a stream of random characters
    #       Pass 6: Writes a stream of random characters
    #       Pass 7: Writes a stream of random characters
    # random data
    #   x passes: random characters
    
