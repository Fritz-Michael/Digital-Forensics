import os

if __name__ == '__main__':
	dir = os.getcwd() + '/sleuthkit-4.5.0-win32/bin'
	os.chdir(dir)
	current = os.getcwd()
	os.system('SETX Path "%Path%;' + current + '"')