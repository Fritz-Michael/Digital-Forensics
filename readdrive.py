import os
import subprocess as sp
import sys
import time

def get_file_system(path):
	temp = sp.check_output(['fsstat',path,'|','findstr','"File System Type:"'],shell=True).decode(sys.stdout.encoding).strip()
	result = temp.split('\n')
	return result[0]


def get_inodes(path):
	temp = sp.check_output(['ils','-e',path],shell=True).decode(sys.stdout.encoding).strip()
	result = temp.split('\n')
	x = 3
	files_list = result[3:]
	inode_list = []
	inode_list = [x.split('|')[0] for x in files_list]
	info_list = [sp.check_output(['ffind',path,x],shell=True).decode(sys.stdout.encoding).strip() for x in inode_list]
	return inode_list

def get_file_info(path,inodes):
	file_list = [sp.check_output(['ffind',path,x],shell=True).decode(sys.stdout.encoding).strip() for x in inodes]
	written = [sp.check_output('istat ' + path + ' ' + x + ' | findstr "Written:"',shell=True).decode(sys.stdout.encoding).strip().strip('Written:\t') for x in inodes]
	accessed = [sp.check_output('istat ' + path + ' ' + x + ' | findstr "Accessed:"',shell=True).decode(sys.stdout.encoding).strip().strip('Accessed:\t') for x in inodes]
	created = [sp.check_output('istat ' + path + ' ' + x + ' | findstr "Created:"',shell=True).decode(sys.stdout.encoding).strip().strip('Created:\t') for x in inodes]
	return (filelist,written,accessed,created)

if __name__ == '__main__':
	# start = time.time()
	# path = '\\\\.\\E:'
	# print(get_file_system(path))
	# print('Total runtime: {}'.format(time.time()-start))
	for x in range(7):
		print(x)