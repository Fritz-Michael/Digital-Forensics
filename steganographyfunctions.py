from stegano import lsb
from stegano import exifHeader


def png_encode(file_name, message, mfile_name):
	secret = lsb.hide(file_name, message)
	secret.save(mfile_name)

def png_decode(mfile_name):
	return lsb.reveal(mfile_name)

def jpg_tiff_encode(file_name, message, mfile_name):
	secret = exifHeader.hide(file_name, mfile_name, secret_message=message)

def jpg_tiff_decode(mfile_name):
	return exifHeader.reveal(mfile_name).decode()