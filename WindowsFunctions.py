import string
import time
import datetime
import os
import platform
import operator
import threading
import binascii
import glob
import sys
from ctypes import windll
import ctypes
from WindowsFunctions import *
import multiprocessing
from multiprocessing import Manager
import struct
from easygui import *
from PyQt5.QtWidgets import QApplication, QProgressBar, QWidget, QPushButton, QMainWindow, QLabel
from PyQt5.QtCore import QBasicTimer, QCoreApplication

#### GLOBAL VARIABLES ####
headerSign = []
footerSign = []
extensionSign = []
fnameMeta = []
dateMeta = []

class App(QMainWindow):
	
	def __init__(self, label):
		super().__init__()
		self.factor = 0.0001
		self.completed = 0
		self.setWindowTitle("FORENSC : Data Carving")
		self.label = QLabel(self)
		self.label.setText(label)
		self.label.move(20, 0)
		self.setMinimumSize(600, 800)
		self.progressBar = QProgressBar(self)
		self.progressBar.setGeometry(40, 40, 550, 25)
		self.btnStart = QPushButton('Start Scanning', self)
		self.btnStart.move(40, 80)
		self.btnStart.clicked.connect(self.startScanning)
		self.show()
	
	def set_factor(self, factor):
		self.factor = factor
	
	def addProgress(self):
		self.completed += self.factor
		self.progressBar.setValue(self.completed)
	
	def startScanning(self):
		self.completed = 0
		while self.completed < 100:
			self.completed += self.factor
			self.progressBar.setValue(self.completed)
		self.close()		
		
### GET CURRENT DRIVES
def get_drivesWin(): 
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

### TOTAL NUMBER OF SECTORS NG DRIVE 
### PARAMETERS 
	#path-'\\\\.\\E:' 
def gettotalsectors(path): 
	drive = open(path,'rb')
	drive.read(40)
	sectors = int.from_bytes(drive.read(8), byteorder='little')
	drive.close()
	return sectors

### GET BYTES PER SECTOR 
### PARAMETERS 
	#path - 'E'
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

### SECTORS PER CLUSTER 
### PARAMETERS 
	#path-'E'
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

### LOCATION NG MASTER FILE TABLE
### PARAMETERS
	#path - '\\\\.\\E:'
	#rootPath - 'E' 
def mftlocation(path, rootPath): 
	drive = open(path,'rb')
	drive.read(48)
	location = int.from_bytes(drive.read(8),byteorder='little')
	location *= getsectorspercluster(rootPath)
	# location *= getbytespersector(rootPath)
	drive.close()
	return location

### converts filetime to datetime object
### PARAMETERS
	#filetime - bytes that represent the filetime
def gettime(filetime):
    Ftime = int(struct.unpack('<Q', filetime)[0])
    Epoch = divmod(Ftime - 116444736000000000, 10000000)
    Actualtime = datetime.datetime.fromtimestamp(Epoch[0])
    return Actualtime.strftime('%Y-%m-%d %H:%M:%S')

### METADATA (CREATED, LAST MODIFIED, LAST ACCESS)
### PARAMETERS
	#path - '\\\\.\\E:'
	#rootPath - 'E'
	#mft - location of the master file table
def getMACtimes(path, rootPath, mft): 
	drive = open(path,'rb')
	drive.seek(int(mft))
	drive.read(80)
	create = drive.read(8)
	modified = drive.read(8)
	access = drive.read(8)
	drive.close()
	return (gettime(create),gettime(modified),gettime(access))

### METADATA (CREATED, LAST MODIFIED, LAST ACCESS)
### PARAMETERS
	#path - '\\\\.\\E:'
	#rootPath - 'E'
	#mft - location of the master file table
def getfilename(path, rootPath, mft):
	drive = open(path,'rb')
	drive.read(1)
	bfile = False
	mft *= getbytespersector(rootPath)
	drive.seek(int(mft))
	fbyte = drive.read(5).decode('utf-8')

	if fbyte == 'FILE*':
		bfile = True

	drive.seek(int(mft))
	fnameattr = b'00000000'

	while fnameattr != b'30000000':
		fnameattr = binascii.hexlify(drive.read(4))

	currfnpos = drive.tell()
	fnsize = drive.read(4)
	fnsize = int.from_bytes(fnsize,byteorder='little')
	drive.seek(currfnpos)
	drive.seek(24, 1)
	drive.read(60)
	namesize = drive.read(1)

	if int.from_bytes(namesize,byteorder='little') > 32 and bfile == False:
		drive.seek(currfnpos)
		drive.read(4)
		fnameattr = b'00000000'

		while fnameattr != b'30000000':
			fnameattr = binascii.hexlify(drive.read(4))

		currfnpos = drive.tell()
		fnsize = drive.read(4)
		fnsize = int.from_bytes(fnsize,byteorder='little')
		drive.seek(currfnpos)
		drive.seek(24, 1)
		drive.read(60)
		namesize = drive.read(1)

		if int.from_bytes(namesize,byteorder='little') > 32:
			drive.close()
			return None

	namesize = int.from_bytes(namesize,byteorder='little')
	drive.read(1)
	filename = drive.read(namesize*2).decode('utf-16')

	if filename.find("~",0, namesize) == -1 and namesize != 0:
		drive.close()
		return filename
	else:
		if namesize == 0:
			drive.close()
			return None

		drive.seek(currfnpos)
		drive.seek(fnsize, 1)
		drive.seek(24, 1)
		drive.read(60)
		namesize = drive.read(1)
		namesize = int.from_bytes(namesize,byteorder='little')
		drive.read(1)
		filename = drive.read(namesize*2).decode('utf-16')
		drive.close()
		return filename

def getmetadata(path, rootpath):
	drive = open(path, 'rb')
	currsec = mftlocation(path, rootpath)
	ncount = 0
	x = 0
	ifMFTtable = True
	print(currsec)
	while ifMFTtable:
		if x == 16:
			currsec += 16
		currboff = getbytespersector(rootpath) * currsec
		drive.seek(currboff)
		fbyte = drive.read(4).decode('utf-8')
		print(fbyte)
		if fbyte == 'FILE':
			print('Current Sector: ',currsec)

			try:
				fname = getfilename(path, rootpath, currsec)
			except UnicodeDecodeError as e:
				fname = None
				print(e)
			except BaseException:
				fname = None

			try:
				fdate = getMACtimes(path, rootpath, currsec)
			except OSError:
				fdate = None
			except BaseException:
				fdate = None

			if fname == None:
				ncount +=1

			if fname != None:
				fnameMeta.append(fname)
				dateMeta.append(fdate)

			x+=1
			currsec += 2
		elif fbyte == 'BAAD':
			currsec += 2
		else:
			ifMFTtable = False
			print('pepe si jarold')
	for x in fnameMeta:
		print(x)
	print('Number of MFT Entries: ',x)	
	print('Number of None: ', ncount)

	drive.close()
	return (fnameMeta, dateMeta)
	
### save the headers signature to headerSign - global variable
def getHeaders():
	with open('headers.txt') as openfileobject:
		for line in openfileobject:
			temp = []
			tempLine = line.split()
			for li in tempLine:
				temp.append(bytes(li,'utf-8'))
			headerSign.append(temp)

### save the footers signature to footerSign - global variable
def getFooters():
	with open('footers.txt') as openfileobject:
		for line in openfileobject:
			temp = []
			tempLine = line.split()
			for li in tempLine:
				temp.append(bytes(li,'utf-8'))
			footerSign.append(temp)

### save the extensions to extensionSign - global variable
def getExtensions():
	with open('extensions.txt', 'r') as openfileobject:
		for line in openfileobject:
			extensionSign.append(line)

### find the signature of the file in the multiple block section
### PARAMETERS
	#path - '\\\\.\\E:'
	#rootPath - 'E'
	#startSector - starting sector
	#endSector - last sector, use gettotalsector function
	#headers - the header of the file type
	#footers - footer of the file type
	#locHolder - list that will contain the position of header and footer
	#additional - docx and xlsx file have an additional 18 offset
def findSignatures(path, rootPath, startSector, endSector, headers, footers, locHolder, additional):
	time.sleep(0.02)
	bytesPerSector = getbytespersector(rootPath)
	sectorPerCluster = getsectorspercluster(rootPath)
	drive = open(path,'rb')
	cur = b'0'
	posHeader = 0
	posFooter = 0
	maxsize = 100
	while startSector < endSector:
		drive.seek(int(bytesPerSector*startSector))
		foundHeader = False
		foundFooter = False
		cur = binascii.hexlify(drive.read(1))
		if cur == headers[0]:
			posHeader = drive.tell()
			nextbyte = cur 
			for header in headers:
				if header == nextbyte:
					nextbyte = binascii.hexlify(drive.read(1))
					foundHeader = True 
				else:
					drive.seek(posHeader, 0)
					foundHeader = False
					break
			if foundHeader:
				size = 0
				while not foundFooter and size != maxsize:
					cur = nextbyte = binascii.hexlify(drive.read(1))
					if nextbyte == footers[0]:
						for footer in footers:
							if footer == cur:
								cur = binascii.hexlify(drive.read(1))
								foundFooter = True
							else:
								foundFooter = False
								break
					size += 1
				posFooter = drive.tell()
		startSector += 1
		if foundHeader and foundFooter:
			print(posHeader,posFooter)
			locHolder.append((posHeader,posFooter+additional))
	print("Im done", threading.current_thread().name)
	drive.close()

### function that will recover files
### PARAMETERS
	#path - '\\\\.\\E:'
	#filepositions - 'list containing the file positions'
	#extension - file extension of the file type to be recovered
def recoverfile(path, filepositions, extension, folder):
	time.sleep(0.02)
	drive = open(path, 'rb')
	for fileposition in filepositions:
		start = fileposition[0]
		end = fileposition[1]
		image = open(folder + '\\found\\' + str(fileposition[0]) + extension, 'wb')
		drive.seek(start-1)
		while start < end:
			cur = drive.read(1)
			image.write(cur)
			start += 1
		image.close()
		print("Saved ", extension, " file!")
	drive.close()

### function that will recover docx and xlsx files
### PARAMETER
	#path - '\\\\.\\E:'
	#filepositions - list of the filepositions containing docx and xlsx
def recoverdocxxlsx(path, filepositions, folder):
	time.sleep(0.2)
	drive = open(path, 'rb')
	isdocx = False
	isxlsx = False
	prev = ''
	for fileposition in filepositions:
		start = fileposition[0]
		end = fileposition[1]
		image = open(folder + '\\found\\' + str(fileposition[0]), 'wb')
		drive.seek(start-1)
		while start < end:
			curPos = drive.tell()
			cur = drive.read(1)

			if binascii.hexlify(cur) == b'77' and not isdocx:
				drive.seek(curPos)
				header = binascii.hexlify(drive.read(5))
				if header == b'776f72642f':
					isdocx = True
					drive.seek(curPos+1)
				else:
					drive.seek(curPos+1)

			if binascii.hexlify(cur) == b'78' and not isxlsx:
				drive.seek(curPos)
				header = binascii.hexlify(drive.read(3))
				if header == b'786c2f':
					isxlsx = True
					drive.seek(curPos+1)
				else:
					drive.seek(curPos+1)

			image.write(cur)
			start += 1
			prev = cur
		image.close()
		if isdocx:
			os.rename(folder + '\\found\\' + str(fileposition[0]), folder + '\\found\\' + str(fileposition[0]) + '.docx')
			print("Saved ", ".docx", " file!")
		if isxlsx:
			os.rename(folder + '\\found\\' + str(fileposition[0]), folder + '\\found\\' + str(fileposition[0]) + '.xlsx')
			print("Saved ", ".xlsx", " file!")

def main():
	threads = 0
	manager = Manager()
	process = []
	locations = manager.list()
	start = time.time()
	### get the file types ###
	getHeaders()
	getFooters()
	getExtensions()
	##########################
	
	### searching for signatures ###
	for x in range(len(headerSign)):
		locations.append(manager.list())

	for x in range(len(headerSign)):
		if extensionSign[x] == '.docx':
			process.append(threading.Thread(target=findSignatures,args=('\\\\.\\E:','E',0,3000000,headerSign[x],footerSign[x],locations[x],20)))
		else:
			process.append(threading.Thread(target=findSignatures,args=('\\\\.\\E:','E',0,3000000,headerSign[x],footerSign[x],locations[x],0)))

	for x in range(len(headerSign)):
		process[x].start()

	for x in range(len(headerSign)):
		process[x].join()
	###############################

	process = []
	startRecover = time.time()
	### recovering files ###
	for x in range(len(headerSign)):
		if extension[x] == '.docx':
			process.append(threading.Thread(target=recoverdocxxlsx,args=('\\\\.\\E:',locations[x])))
		else:
			process.append(threading.Thread(target=recoverfile,args=('\\\\.\\E:',locations[x],extensionSign[x].rstrip())))

	for x in range(len(headerSign)):
		process[x].start()

	for x in range(len(headerSign)):
		process[x].join()
	########################
	print("total recover time: ", time.time()-startRecover)

	print("total time: ", time.time()-start)

def bulalords():
	hack = "hacker.jpg"
	baywatch = "baywatch.jpg"
	tech = "gtx1080.png"
	waitScanning = "Finish Scanning first"
	msgActivity = "Wait for the files to recover before pressing next"
	msgMenu = "Set The Parameters For a Customized Retrieving"
	msgMetadata = "This is all the metadata you have recovered"
	msgDrive = "Welcome, I am the File Retriever-\nThis is the list of Active Drives\n\nSelect the directory that contains the deleted file you want to recover\nTo exit, click the CANCEL button or press the ESC key."
	msgSelectImage = "Select an Image file to preview"
	msgPreview = "This is the preview of the selected image"
	msgDataType = "Welcome, I am the File Retriever-\nThis is your list of retrievable file types\n\nSelect the data types you want recovered. \nTo exit, click the CANCEL button or press the ESC key."
	msgImage = "Welcome, I am the File Retriever-\nThis is your list of images you have recovered\n\nSelect an image to preview it's photo.\nTo exit, click the CANCEL button or press the ESC key."
	reply = "Back to Drive List"
	msgThreader = "Input Thread Count"
	msgFolder = "Select Directory To Save Files Recovered" 
	msgOpenDirectory = "Open the directory you want to open"
	msgFileRecovered = "These are all the files you have recovered"
	msgStartSector = "Please input starting sector #"
	msgEndSector = "Please input ending sector #"
	title = "FILE RETRIEVER"
	dataTypeOptions = ['JPG','PNG','PDF','DOC','DOCX','XLS','XLSX']
	chosenFiles = []
	directoryHere = []
	chosenMenuButton = 0
	chosenMenu2Button = 0
	menuOption = ["Start Retrieving", "Data Types to Recover", "Enter Starting Sector", "Enter Ending Sector", "Locate The Directory You Want Files Recovered", "Select Directory You Want Recovered Files Saved", "Exit Program"]
	menu2Option = ["Restart Program", "Recovered File Name Lists", "Image File List", "All files recovered", "Exit Program"]
	choosingFile= [hack,baywatch, tech]
	imageList = []
	fileListRecovered = []
	dataTypes = None
	rootPath = None
	dirSave = None
	imageChoices = ["Return", "Exit Program"]
	dataTypeError = "Please choose atleast 1 data type to recover"
	dirSavingFile = "Please choose a directory to save files recovered"
	dirRecoverFile = "Please choose a directory you want files recovered"
	directoryHere = get_drivesWin()
	getHeaders()
	getFooters()
	getExtensions()
	#print(len(headerSign))
	while chosenMenuButton != 1:
		chosenMenuButton = buttonbox(title, msgMenu, image="9328518_orig.png", choices = menuOption)
		if chosenMenuButton == menuOption[0]:
			if dataTypes != None:
				if dirSave != None:
					if rootPath != None:
						#app = QApplication(sys.argv)
						#appMe = App()
						#appMe.show()
						
						
						### recover files here
						process = []
						startRecover = time.time()
						
						index = []
						for type in dataTypes:
							y = 0
							for ext in extensionSign:
								if ext == type:
									index.append(y)
									y += 1
									
						start = time.time()
						### recovering files ###
						for x in range(len(index)):
							if extensionSign[index[x]] == '.docx':
								process.append(multiprocessing.Process(target=recoverdocxxlsx,args=(path,locations[index[x]],dirSave)))
							else:
								process.append(multiprocessing.Process(target=recoverfile,args=(path,locations[index[x]],extensionSign[index[x]].rstrip(),dirSave)))

						for x in range(len(index)):
							process[x].start()
						
						for x in range(len(index)):
							process[x].join()
						########################
						print("total recover time: ", time.time()-start)
						
						dirSavePng = dirSave + '//found' + "/*.png"
						for imageName in glob.glob(dirSavePng):
							imageList.append(imageName)
							fileListRecovered.append(imageName)
						dirSaveJpg = dirSave + '//found' + "/*.jpg"
						for imageName in glob.glob(dirSaveJpg):
							imageList.append(imageName)
							fileListRecovered.append(imageName)
						dirSavePdf = dirSave + '//found' +"/*.pdf"
						for fileName in glob.glob(dirSavePdf):
							fileListRecovered.append(fileName)
						dirSaveDoc = dirSave + '//found' + "/*.doc"
						for fileName in glob.glob(dirSaveDoc):
							fileListRecovered.append(fileName)
						dirSaveDocx = dirSave + '//found' + "/*.docx"
						for fileName in glob.glob(dirSaveDocx):
							fileListRecovered.append(fileName)
						dirSaveXls = dirSave + '//found' + "/*.xls"
						for fileName in glob.glob(dirSaveXls):
							fileListRecovered.append(fileName)
						dirSaveGif = dirSave + '//found' + "/*.gif"
						for fileName in glob.glob(dirSaveGif):
							fileListRecovered.append(fileName)
						dirSaveRtf = dirSave + '//found' + "/*.rtf"
						for fileName in glob.glob(dirSaveRtf):
							fileListRecovered.append(fileName)
						while chosenMenu2Button != 1:
							chosenMenu2Button = buttonbox(title, msgMenu, image="9328518_orig.png", choices = menu2Option)
							if chosenMenu2Button == menu2Option[0]:
								chosenMenu2Button = 1 
							elif chosenMenu2Button == menu2Option[1]:
								nameList= choicebox(msgMetadata, title, imageList)
							elif chosenMenu2Button == menu2Option[3]:
								filesListed= choicebox(msgFileRecovered, title, fileListRecovered)
							elif chosenMenu2Button == menu2Option[2]:
								imageChosen = choicebox(msgImage, title, imageList)
								if imageList:
									reply = buttonbox(msg = "This is the preview of the image", image=imageChosen, choices=imageChoices)
									if reply == imageChoices[1]:
										exit()
							elif chosenMenu2Button == menu2Option[4]:
								exit()
								
					else:
						error1 = msgbox(dirRecoverFile, title, ok_button='RETURN')
				else:
					error2 = msgbox(dirSavingFile, title, ok_button='RETURN')
			else:
				error3 = msgbox(dataTypeError, title, ok_button='RETURN')
		elif chosenMenuButton == menuOption[1]:
			dataTypes= multchoicebox(msgDataType, title, extensionSign)
		elif chosenMenuButton == menuOption[2]:
			startSector = integerbox(msgStartSector, title,  default=0, lowerbound=0, upperbound=9999999) ### STARTING SECTOR HERE
		elif chosenMenuButton == menuOption[3]:
			endSector = integerbox(msgEndSector, title,  default=0, lowerbound=0, upperbound=9999999) ### ENDING SECTOR HERE
		elif chosenMenuButton == menuOption[4]:
			rootPath = choicebox(msgDrive, title, directoryHere)
			
			path = '\\\\.\\' + rootPath + ':'
			str(path)
			print(path)
			manager = Manager()
			process = []
			locations = manager.list()
			start = time.time()
			### searching for signatures ###
			for x in range(len(headerSign)):
				locations.append(manager.list())
			start = time.time()
			for x in range(len(headerSign)):
				if extensionSign[x] == '.docx':
					process.append(multiprocessing.Process(target=findSignatures,args=(path,rootPath,0,gettotalsectors(path),headerSign[x],footerSign[x],locations[x],20)))
				else:
					process.append(multiprocessing.Process(target=findSignatures,args=(path,rootPath,0,gettotalsectors(path),headerSign[x],footerSign[x],locations[x],0)))
	
			for x in range(len(headerSign)):
				process[x].start()
			for x in range(len(headerSign)):
				process[x].join()
			###############################
			
			metadata = getmetadata(path,rootPath)
			print('Drive scanning took:', time.time()-start)
			print(metadata[1][0])
			
		elif chosenMenuButton == menuOption[5]:
			dirSave = diropenbox(msgFolder, title)
			os.mkdir(dirSave + '\\found')
		elif chosenMenuButton == menuOption[6]:
			exit()
			
if __name__ == '__main__':
	bulalords()